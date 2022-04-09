from flask import Flask, request, Response
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
import copy
import time

app = Flask(__name__)

data_list = ['status', 'title', 'date', 'starting_time', 'meeting_point', 'distance', 'speed', 'ending_place'
    , 'route', 'remark', 'chat_id']
initial_user = {data: 'none' for data in data_list}

message_dict = {data: 'none' for data in data_list}
message_dict['title'] = 'Let\'s create a new ride. First, send me the <b>title</b> of the ride'
message_dict['date'] = 'Please send me the <b>date</b> of the ride.'
message_dict['starting_time'] = 'Please send me the <b>starting time</b>.'
message_dict['meeting_point'] = 'Let me know the <b>meeting point</b>.'
message_dict['distance'] = 'What is the <b>total distance</b> the ride?'
message_dict['speed'] = 'What is the <b>expected speed range</b>?'
message_dict['ending_place'] = 'Where will the ride <b>end</b>?'
message_dict['route'] = 'If you have the full <b>route</b>, please send me here.'
message_dict['remark'] = 'Are there any other remarks?'

welcome_text = 'Welcome to <b>cyclist_bot</b>! Please user <b>/start</b> to create a ride.'
post_text = '<strong>%s</strong>\n\n' \
            '<b>Date: </b>%s\n<b>Starting Time: </b>%s\n' \
            '<b>Meeting Point: </b>%s\n\n' \
            '<b>Distance: </b>%s\n' \
            '<b>Speed: </b>%s\n\n' \
            '<b>Ending Point: </b>%s\n' \
            '<b>Route: </b>%s\n' \
            '<b>Other Remark: </b>%s\n\n' \
            '<i>Created using @join_ride_bot</i>'

posts = dict()
users_in_progress = dict()

# Inline_keyboards
KB_DONT_INCLUDE = [
    [InlineKeyboardButton('Do not include a title', callback_data='no_title_ride')],
]
KB_RIDE_POST = [
    [InlineKeyboardButton('Join the ride!', callback_data='join_the_ride')],
    [InlineKeyboardButton('Add to calendar', url='google.com')],
]
KB_RIDE_FINISHED = [
    [InlineKeyboardButton('Publish the ride')]
]
bot = Bot(token='5141401503:AAEt15IjUC11EjqqNw4TElPLq-p9B1ZOV00')


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        update = Update.de_json(request.get_json(force=True), bot)
        print(update)
        if not update.message or not update.message.text:
            return Response('Ok', status=200)

        handle_message(update.message.text, update.message.chat.id)
        return Response('Ok', status=200)

    else:
        return "<p>hi</p>"


def handle_message(text, chat_id):
    if chat_id in users_in_progress:
        user_status = users_in_progress[chat_id]['status']
        print(chat_id)

        users_in_progress[chat_id][user_status] = text
        print(users_in_progress)

        user_status_index = data_list.index(user_status)
        if user_status_index < len(data_list) - 2:
            users_in_progress[chat_id]['status'] = data_list[user_status_index + 1]
            send_message(chat_id, text=message_dict[users_in_progress[chat_id]['status']])
        else:
            #users_in_progress[chat_id]['chat_id'] = chat_id
            #timestamp = time.time()
            #posts[chat_id + str(timestamp)] = users_in_progress[chat_id]
            complete_message = post_text % (users_in_progress[chat_id]['title'], users_in_progress[chat_id]['date'], users_in_progress[chat_id]['starting_time'],
                                            users_in_progress[chat_id]['meeting_point'], users_in_progress[chat_id]['distance'], users_in_progress[chat_id]['speed'],
                                            users_in_progress[chat_id]['ending_place'], users_in_progress[chat_id]['route'], users_in_progress[chat_id]['remark'])

            send_message(chat_id, text=complete_message)
            send_message(chat_id, text='Copy and paste to your ride group and let others join your ride! Use /start to post another ride.')
            users_in_progress.pop(chat_id)

    elif text.startswith('/start'):
        #send_message(chat_id, text=message_dict['title'], reply_markup=InlineKeyboardMarkup(KB_DONT_INCLUDE))
        send_message(chat_id, text=message_dict['title'])
        temp_status = copy.copy(initial_user)
        temp_status['status'] = 'title'
        users_in_progress[chat_id] = temp_status

    else:
        send_message(chat_id, text=welcome_text)

    chat_id = 0
    text = 0


def send_message(chat_id, text, **kwargs):
    if 'reply_markup' in kwargs:
        bot.sendMessage(chat_id=chat_id, text=text, parse_mode='html', reply_markup=kwargs['reply_markup'])
    else:
        bot.sendMessage(chat_id=chat_id, parse_mode='html', text=text)
    return

if __name__ == '__main__':
    app.run(debug=True, threaded=False, processes=True)
