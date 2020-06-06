import random
from flask import Flask, request
from pymessenger.bot import Bot
import csv
import os
import time

app = Flask(__name__)

ACCESS_TOKEN = os.environ['EAAp08CWbor8BAGliVzZCXABn0GuwRZAI3S3PZBVHGUyhhIAXI3V8XK6mPuXTs1yvusjMZCEZAKrtJN6kZBK1XcmKOORbXAbmqnmLGC3avmJAPHy9rlZAbbzPStghnv9jXEEsB98y3eJccndEZCI3sm4p6jskWbhetsZCEq5NKjCPqKOlhYJ0XNQtAJCckf0HlfkkZD']
VERIFY_TOKEN = os.environ['12345']

bot = Bot(ACCESS_TOKEN)

#Получать сообщения, посылаемые фейсбуком нашему боту мы будем в этом терминале вызова
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
    # до того как позволить людям отправлять что-либо боту, Facebook проверяет токен,
    # подтверждающий, что все запросы, получаемые ботом, приходят из Facebook
        token_sent = request.args['hub.verify_token']
        return verify_fb_token(token_sent)
    # если запрос не был GET, это был POST-запрос и мы обрабатываем запрос пользователя
    else:
        # получаем сообщение, отправленное пользователем для бота в Facebook
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                #определяем ID, чтобы знать куда отправлять ответ
                    recipient_id = message['sender']['id']
                if message['message'].get('text'):
                	
                	body = message['message'].get('text')
                	if body.lower() == 'парсинг':
                		os.system('python pr.py')
                		time.sleep(1)
                		response_sent_text = get_message()
                		send_message(recipient_id, response_sent_text)
                	elif body.lower() == 'help':
                		response_sent_text = 'Для того чтобы вывести все посты сообщества введите "парсинг", для последнего поста введите "пост"'
                		send_message(recipient_id, response_sent_text)
                	elif body.lower() == 'пост':
                		os.system('python pr.py')
                		time.sleep(1)
                		response_sent_text = get_message2()
                		send_message(recipient_id, response_sent_text)
                	else:
                		response_sent_text = 'я тебя не понимаю, для помощи введите help'
                		send_message(recipient_id, response_sent_text)
                #если пользователь отправил GIF, фото, видео и любой не текстовый объект
                if message['message'].get('attachments'):
                    response_sent_nontext = 'я тебя не понимаю, для помощи введите help'
                    send_message(recipient_id, response_sent_nontext)
        return "Message Processed"

def verify_fb_token(token_sent):
    '''Сверяет токен, отправленный фейсбуком, с имеющимся у вас.
    При соответствии позволяет осуществить запрос, в обратном случае выдает ошибку.'''
    if token_sent == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return 'Invalid verification token'

def send_message(recipient_id, response):
    '''Отправляет пользователю текстовое сообщение в соответствии с параметром response.'''
    bot.send_text_message(recipient_id, response)
    return 'Success'

def get_message():
	vivod = ''
	csv_path = "cars.csv"
	with open(csv_path, "r") as f_obj:
		reader = csv.reader(f_obj)
		for row in reader:
			s = " ".join(row)
			s = s.replace(';;',';')
			s = s.replace(';',"\n")
			vivod += s
			vivod += "\n"
		return (vivod)


def get_message2():
	vivod = ''
	csv_path = "cars.csv"
	with open(csv_path, "r") as f_obj:
		reader = csv.reader(f_obj)
		for row in reader:
			s = " ".join(row)
			s = s.replace(';;',';')
			s = s.replace(';',"\n")
			vivod += s
			return (vivod)



if __name__ == '__main__':
    app.run(port=5000, use_reloader = True)
