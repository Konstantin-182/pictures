import telebot
import timm
from train import TrainModel

# Токен вашего бота
token = '7264686704:AAFbD4Kz4JcXGSqoYEjUkql-7a-DDGMbQUE'
bot = telebot.TeleBot(token=token)

# Инициализация модели
ml = TrainModel()

def output_text(res_soft_max):
    str_f = ''
    for _acter, _res_soft_max in zip(ml.acters, res_soft_max):
        str_f += f'{_acter}: {round(_res_soft_max * 100, 3)} %\n'
    return str_f

@bot.message_handler(content_types=['photo'])
def photo(message):
    try:
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)

        bot.send_message(message.chat.id, "Картинка получена")

        with open("image.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)

        res_soft_max, res_argmax = ml.classify_image('image.jpg')
        bot.send_message(message.chat.id, f'Это актер {ml.acters[res_argmax]}')
        bot.send_message(message.chat.id, output_text(res_soft_max))

    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Отправьте картинку.")

@bot.message_handler()
def send_text(message):
    bot.send_message(message.chat.id, 'Я не понимаю')

bot.polling()
