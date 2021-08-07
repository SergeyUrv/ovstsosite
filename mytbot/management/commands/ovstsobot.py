from django.core.management.base import BaseCommand
import telebot
from telebot import types
from mytbot.models import People, Tempa
import re
import datetime

bot = telebot.TeleBot('1949325348:AAHvsy8MwDfJJG1bD1QiuZey_YFYhKZoMCg', parse_mode=None)

@bot.message_handler(content_types=['contact'])
def get_test(message):
    # Эти параметры для клавиатуры необязательны, просто для удобства
    # keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    # button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    # button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    # keyboard.add(button_phone, button_geo)
    # bot.send_message(message.chat.id,
    #                  "Отправь мне свой номер телефона или поделись местоположением, жалкий человечишка!",
    #                  reply_markup=keyboard)
    bot.send_message(message.from_user.id, message.contact.phone_number)

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
                         "Привет! Я бот отдела взаимодействия с ТСО, чтобы я узнал тебя отправь мне свой номер телефона",
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

def get_temp(message):  # получаем температуру
    try:
        item_peop = People.objects.get(id_telegramm=message.from_user.id)
        try:
            temps = float(message.text)  # проверяем, что температура введена корректно
            commit_temp(temps=temps, message=message, item_peop=item_peop)
        except Exception:
            bot.send_message(message.from_user.id,
                             'Цифрами, пожалуйста! Напишите дробное число через точку, например - 36.6')
            bot.register_next_step_handler(message, get_temp)
    except People.DoesNotExist:
        return start_command

#идентификация по номеру телефона
@bot.message_handler(content_types=['contact'])
def get_phone(message):
        if message.contact.user_id == message.from_user.id:
            try:
                ctel=re.sub("^7", "+7", message.contact.phone_number)
                item = People.objects.get(cont_tel=ctel)
                item.id_telegramm = message.contact.user_id
                item.save()
                bot.send_message(message.from_user.id, "Я узнал тебя! Чтобы узнать что я умею набери /help")
                bot.register_next_step_handler(message, help_command)
            except People.DoesNotExist:
                bot.send_message(message.from_user.id, message.contact.phone_number+" - я не узнал тебя! Обратись к администратору бота.")
        else:
            bot.send_message(message.from_user.id, "Это не твой номер телефона, обманывать нехорошо!")

#помощь
@bot.message_handler(commands=['help'])
def help_command(message):
        bot.send_message(message.from_user.id, "Команды бота: /help - все команды бота \n"
                                               "/temp - передать температуру\n"
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
        bot.send_message(message.chat.id, "Доброе утро " + item_peop.fio_name + ", твоя температура " + str(temps) + " записана")

class Command(BaseCommand):

    #слушаем чат
    @bot.message_handler(content_types=['text'])
    def start(message):
        temp = re.findall('^Доброе утро.*\s(\d\d.\d)$', message.text)
        if not temp:
            temp = re.findall('^\d\d.\d$', message.text)
        if temp:
            try:
                item = People.objects.get(id_telegramm=message.from_user.id)
                temp = re.sub(",", ".", temp[0])
                commit_temp(temps=float(temp), message=message, item_peop=item)
            except People.DoesNotExist:
                bot.send_message(message.chat.id, "Чтобы писать тут свою температуру зарегитрируйтесь в боте @OVsTSO_bot")
        # elif message.text == '/help':
        #     bot.send_message(message.from_user.id, "Комманды: /help - все команды бота \n"
        #                                            "/temp - передать температуру")
        # elif message.text == '/test':
        #     bot.send_message(message.from_user.id, "номер телефона")
        #     bot.register_next_step_handler(message, get_test)
        elif message.text == '/temp':
            bot.send_message(message.from_user.id, "Какая температура тела у Вас сегодня?")
            bot.register_next_step_handler(message, get_temp)  # следующий шаг – функция get_name
        # else:
        #     bot.send_message(message.from_user.id, 'Напиши /help')



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