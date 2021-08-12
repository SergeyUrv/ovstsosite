from django.core.management.base import BaseCommand
import telebot
from telebot import types
from mytbot.models import People, Tempa, Kalendar
import re
import datetime
from django.conf import settings
import schedule
from threading import Thread
from time import sleep
import pandas as pd

bot = telebot.TeleBot(settings.TELEGRAM_TOKEN_BOT, parse_mode=None)

# @bot.message_handler(content_types=['contact'], func=lambda message: message.chat.id > 0)
# def get_test(message):
#     # Эти параметры для клавиатуры необязательны, просто для удобства
#     # keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#     # button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
#     # button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
#     # keyboard.add(button_phone, button_geo)
#     # bot.send_message(message.chat.id,
#     #                  "Отправь мне свой номер телефона или поделись местоположением, жалкий человечишка!",
#     #                  reply_markup=keyboard)
#     bot.send_message(message.from_user.id, message.contact.phone_number)

##старт бота
@bot.message_handler(commands=['start'], func=lambda message: message.chat.id > 0)
def start_command(message):
    try:
        item = People.objects.get(id_telegramm=message.from_user.id)
        bot.send_message(message.from_user.id, item.fio_name+", мы с тобой уже знакомы. Чтобы узнать что я умею набери /help")
        bot.register_next_step_handler(message, help_command)
    except People.DoesNotExist:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
        keyboard.add(button_phone)
        bot.send_message(message.chat.id,
                         "Привет! Я бот отдела взаимодействия с ТСО, чтобы я узнал тебя отправь мне свой номер телефона нажав на кнопку \"Отправить номер телефона\"",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, get_phone)

@bot.message_handler(commands=['report'])
def temp_view(message):
    msg='Доброе утро! \nОВсТСО:\n'
    for p in People.objects.all():
        try:
            #ищем последнюю внесенную температуру
            ptemp=Tempa.objects.filter(sname=p, created_date__gte=datetime.date.today()).order_by('-created_date')[:1].get().temp
        except Tempa.DoesNotExist:
            ptemp = '-'
        msg = msg+p.fio_sname+' '+str(ptemp)+"\n"
    bot.send_message(message.chat.id,msg)

# @bot.message_handler(commands=['otchet'])
# def otchet(message):
#     get_otchet()
#     bot.send_message(message.chat.id, 'Готово!')

def get_temp(message):  # получаем температуру
    try:
        item_peop = People.objects.get(id_telegramm=message.from_user.id)
        try:
            temps = float(re.sub(",", ".", message.text))  # проверяем, что температура введена корректно
            commit_temp(temps=temps, message=message, item_peop=item_peop)
            try:
                # ищем отгул
                otgul = Kalendar.objects.filter(name=item_peop, day__exact=datetime.date.today()).exclude(type__exact='раб').order_by('-created_date')[:1].get()
                bot.send_message(message.from_user.id, item_peop.fio_name+', приятно, что в свой ' + otgul.get_type_display() + ' - ' + otgul.comment + ' Вы решили пойти в офис на работу)')
            except Kalendar.DoesNotExist:
                pass
        except Exception:
            bot.send_message(message.from_user.id,
                             'Цифрами, пожалуйста! Напишите дробное число, например - 36.6')
            bot.register_next_step_handler(message, get_temp)
    except People.DoesNotExist:
        return start_command

#идентификация по номеру телефона
@bot.message_handler(content_types=['contact'], func=lambda message: message.chat.id > 0)
def get_phone(message):
    try:
        if message.contact.user_id == message.from_user.id:
            try:
                ctel=re.sub("^7", "+7", message.contact.phone_number)
                item = People.objects.get(cont_tel=ctel)
                item.id_telegramm = message.contact.user_id
                item.save()
                bot.send_message(message.from_user.id, "Я узнал тебя! Чтобы узнать что я умею набери /help", reply_markup=types.ReplyKeyboardRemove())
                bot.register_next_step_handler(message, help_command)
            except People.DoesNotExist:
                bot.send_message(message.from_user.id, message.contact.phone_number+" - я не узнал тебя! Обратись к администратору бота.", reply_markup=types.ReplyKeyboardRemove())
        else:
            bot.send_message(message.from_user.id, "Это не твой номер телефона, обманывать нехорошо!")
    except:
        bot.send_message(message.from_user.id, "Так не пойдёт! Прото нажми кнопку  \"Отправить номер телефона\" или набери /start, чтобы начать всё сначала")

#помощь
@bot.message_handler(commands=['help'])
def help_command(message):
        bot.send_message(message.from_user.id, "Команды бота: /help - все команды бота \n"
                                               "/report - отчет по температуре за сегодня")
#функция сохранения температуры
def commit_temp(temps, message, item_peop):
    item_temp = Tempa(sname=item_peop, temp=temps)
    item_temp.save()
    if temps < 34:
        bot.send_message(message.chat.id,'Что то Вы слишком холодны сегодня, ' + str(temps) + ' это низкая температура для человека, держите градустник дольше!')
    elif temps > 37:
        bot.send_message(message.chat.id,'Охо-хо: ' + str(temps) + ' это высоковато, может Вам остаться дома сегодня? Свяжитесь с Вашим руководителем по этому вопросу.')
    else:
        bot.send_message(message.chat.id, "Доброе утро, " + item_peop.fio_name + ", твоя температура " + str(temps) + " записана.")

#слушаем чат
@bot.message_handler(content_types=['text'])
def start(message):
    temp = re.findall('^Доброе утро.*\s(\d\d.\d)$', message.text)
    if not temp:
        temp = re.findall('^\d\d.\d$', message.text)
    if not temp:
        temp = re.findall('^Всем привет.*\s(\d\d.\d)$', message.text)
    if temp:
        try:
            item = People.objects.get(id_telegramm=message.from_user.id)
            temp = re.sub(",", ".", temp[0])
            commit_temp(temps=float(temp), message=message, item_peop=item)
            #проверяем в отгуле ли человек
            try:
                # ищем отгул
                otgul = Kalendar.objects.filter(name=item, day__lte=datetime.date.today(), day_end__gte=datetime.date.today()).exclude(type__exact='раб').order_by('-created_date')[:1].get()
                bot.send_message(message.chat.id, item.fio_name+', приятно, что в свой ' + otgul.get_type_display() + ' ' + otgul.comment + ' Вы решили пойти в офис на работу)')
            except Kalendar.DoesNotExist:
                pass
            check_otgul_zavtra(message=message, p=item)
        except People.DoesNotExist:
            bot.send_message(message.chat.id, "Чтобы писать тут свою температуру зарегитрируйтесь в боте @OVsTSO_bot")
    # elif message.text == '/help':
    #     bot.send_message(message.from_user.id, "Комманды: /help - все команды бота \n"
    #                                            "/temp - передать температуру")
    # elif message.text == '/test':
    #     bot.send_message(message.from_user.id, "номер телефона")
    #     bot.register_next_step_handler(message, get_test)
    # elif message.text == '/temp':
    #     bot.send_message(message.from_user.id, "Какая температура тела у Вас сегодня?")
    #     bot.register_next_step_handler(message, get_temp)  # следующий шаг – функция get_name
    # else:
    #     bot.send_message(message.from_user.id, 'Напиши /help')

def check_otgul_zavtra(message,p):
    msg=''
    try:
        #ищем отгул или отпуск
        if datetime.date.today().weekday()==4:
            otgul=Kalendar.objects.filter(name=p, day__lte=(datetime.date.today()+datetime.timedelta(days=3)), day_end__gte=(datetime.date.today()+datetime.timedelta(days=3))).order_by('-created_date')[:1].get()
            if otgul.day != otgul.day_end:
                msg = p.fio_name + ' ' + p.fio_lname + ', спешу напомнить, у Вас с '+ otgul.day.strftime("%d.%m.%Y")+' ' + otgul.get_type_display() + ' (' + otgul.comment + ') до ' + otgul.day_end.strftime("%d.%m.%Y")
            else:
                msg=p.fio_name+' '+ p.fio_lname +', спешу напомнить, в понедельник у Вас '+ otgul.get_type_display() + ' (' + otgul.comment + ')'
        else:
            otgul=Kalendar.objects.filter(name=p,  day__lte=(datetime.date.today()+datetime.timedelta(days=1)), day_end__gte=(datetime.date.today()+datetime.timedelta(days=1))).order_by('-created_date')[:1].get()
            if otgul.day != otgul.day_end:
                msg = p.fio_name + ' ' + p.fio_lname + ', спешу напомнить, у Вас с '+ otgul.day.strftime("%d.%m.%Y") +' ' + otgul.get_type_display() + ' (' + otgul.comment + ') до ' + otgul.day_end.strftime("%d.%m.%Y")
            else:
                msg=p.fio_name+' '+ p.fio_lname +', спешу напомнить, завтра у Вас '+ otgul.get_type_display() + ' (' + otgul.comment + ')'
        bot.send_message(message.chat.id, msg)
    except Kalendar.DoesNotExist:
        pass

# def get_otchet():
#     p=People.objects.all()
#     ptemp = Tempa.objects.filter(created_date__gte=datetime.date.today())
#     df = pd.DataFrame(list(ptemp))
#     df.to_excel("output.xlsx", index=False)


###### планировщик заданий бота
some_id=477234400
def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)

def function_to_run():
    return bot.send_message(some_id, "This is a message to send.")


# Create the job in schedule.
#schedule.every(15).seconds.do(function_to_run)

# Spin up a thread to run the schedule check so it doesn't block your bot.
# This will take the function schedule_checker which will check every second
# to see if the scheduled job needs to be ran.
#Thread(target=schedule_checker).start()


class Command(BaseCommand):


    def get_age(message):
        global age
        while age == 0:  # проверяем что возраст изменился
            try:
                age = int(message.text)  # проверяем, что возраст введен корректно
            except Exception:
                bot.send_message(message.from_user.id, 'Цифрами, пожалуйста');
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
        keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):
        if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
            # код сохранения данных, или их обработки
            bot.send_message(call.message.chat.id, 'Запомню : )')
        elif call.data == "no":
            pass  # переспрашиваем


    bot.polling()


    def handle(self, *args, **options):
        import this