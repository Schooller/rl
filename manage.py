import telebot
from telebot import types
from time import sleep
import app.config as config
import app.functions as functions

bot = telebot.AsyncTeleBot(config.TELEGRAM_TOKEN)



@bot.message_handler(commands=['start'])
def start_command(message):
    sleep(0.1)
    bot.send_message(message.chat.id, 'Доброго дня. Голосування триватиме з 8:55 до 13:45. Введіть свій індивідуальний код. Формат (XXX-XXX)')


@bot.message_handler(commands=['exit'])
def exit_command(message):
    if not message.chat.id == 395809791:
        return
    sleep(0.1)
    if config.isWork:
        config.isWork = False
    else:
        config.isWork = True
    bot.send_message(message.chat.id, str(config.isWork))


@bot.message_handler(commands=["look"])
def look_command(message):
    if not message.chat.id == 395809791:
        return
    sleep(0.1)
    try:
        bot.send_message(message.chat.id, functions.look(message.text.split(" ")[1]))
    except:
        bot.send_message(message.chat.id,'No')


@bot.message_handler(commands=['admin'])
def admin_command(message):
    sleep(0.1)
    if not message.chat.id == 395809791:
        return
    try:
        command, name, key = list(map(str, message.text.split(" ")))
        if functions.admin_send_answer(name, key):
            bot.send_message(message.chat.id,'OK')
        else:
            bot.send_message(message.chat.id,'BAD')
    except:
        bot.send_message(message.chat.id,'BAD')


@bot.message_handler(content_types=["text"])
def answer_message(message):
    sleep(0.1)
    if functions.check_message(message.text):
        if not functions.check_code(message.text, str(message.chat.id)):
            return
        functions.commit_key(message.text, str(message.chat.id))
        name = functions.get_name(str(message.chat.id))
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text="Детальніше...", url=config.MAIN_URL)
        keyboard.add(callback_button)
        bot.send_message(message.chat.id, name + ', дякуємо за інтерес до життя Рішельєвського ліцею! Ознайомитися з програмою наших кандидатів можна тут.', reply_markup=keyboard)
        keyboard = types.InlineKeyboardMarkup()
        sleep(0.1)
        keyboard.add(types.InlineKeyboardButton(text='Анастасия Гуренко', callback_data='Анастасия Гуренко'))
        keyboard.add(types.InlineKeyboardButton(text='Генч Деніз', callback_data='Генч Деніз'))
        keyboard.add(types.InlineKeyboardButton(text='Шиндер Михайло', callback_data='Шиндер Михайло'))
        if not config.isWork:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info+'Голосування не йде. Голосування за Віце-президента парламенту Рішельєвського ліцею. Натисніть щоб вибрати кандидата, у вас ще буде можливість змінити рішення протягом 3 хвилин.', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'Голосування за Віце-президента парламенту Рішельєвського ліцею. Натисніть щоб вибрати кандидата, у вас ще буде можливість змінити рішення.', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    sleep(0.1)
    if call.message:
        """
        if not functions.check_time(str(call.message.chat.id)):
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="На жаль відповіді більше не приймаються, ще раз дякуємо.")
            return
        """
        info = ''
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Анастасия Гуренко', callback_data='Анастасия Гуренко'))
        keyboard.add(types.InlineKeyboardButton(text='Генч Деніз', callback_data='Генч Деніз'))
        keyboard.add(types.InlineKeyboardButton(text='Шиндер Михайло', callback_data='Шиндер Михайло'))
        if not config.isWork:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info+'Голосування не йде. Голосування за Віце-президента парламенту Рішельєвського ліцею. Натисніть щоб вибрати кандидата, у вас ще буде можливість змінити рішення протягом 3 хвилин.', reply_markup=keyboard)
            return
        if call.data == 'Анастасия Гуренко':
            info = 'Ви проголосували за Анастасию Гуренко. '
            functions.send_answer(str(call.message.chat.id), 'Анастасия Гуренко')
        elif call.data == 'Генч Деніз':
            info = 'Ви проголосували за Генча Деніза. '
            functions.send_answer(str(call.message.chat.id), 'Генч Деніз')
        elif call.data == 'Шиндер Михайло':
            info = 'Ви проголосували за Шиндера Михайла. '
            functions.send_answer(str(call.message.chat.id), 'Шиндер Михайло')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info+'Голосування за Віце-президента парламенту Рішельєвського ліцею. Натисніть щоб вибрати кандидата, у вас ще буде можливість змінити рішення.', reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)
