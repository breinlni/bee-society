import os

from flask import Flask, request, render_template, flash, redirect
from handler import handle_yes_no
from log_writer import write_temp_log, write_new_log, close_temp_log
from flask_sqlalchemy import SQLAlchemy
from google.cloud import texttospeech, speech, dialogflow
from stt import detect_intent_audio, detect_intent_texts, speech_to_text
from tts import play_text
from utils import build_standard_response, build_response_with_context

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './keys/beesociety-qjhf-89d43a20a461.json'

tts_client = texttospeech.TextToSpeechClient()

app = Flask(__name__)


# Define Database connection

working_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.sqlite3'
db = SQLAlchemy(app)


class Todos(db.Model):
    """
    Class represents an object for the database
    """
    id = db.Column('ID', db.Integer, primary_key=True)
    todo = db.Column('Todo', db.String)

    def __init__(self, todo):
        self.todo = todo


@app.route('/')
def index():
    """
    Renders start page
    """
    return render_template('recorder.html')


@app.route('/save-record', methods=['POST'])
def record_audio():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    file_name = 'test.mp3'
    file.save(f'./{file_name}')
    intent = detect_intent_audio(file_name)
    return '<h1>Success</h1>'


@app.route('/', methods=['POST'])
def webhook():
    """
    Endpoint for the Dialogflow API
    :return: The JSON response object that gets sent back to Dialogflow
    """
    payload = request.json
    user_response = (payload['queryResult']['queryText'])
    bot_response = (payload['queryResult']['fulfillmentText'])

    play_text(tts_client, bot_response)

    # Write Logs of the conversation for debugging
    write_temp_log(f'User: {user_response}')
    write_temp_log(f'Bot: {bot_response}')

    json_response_object = handle_intent(payload)

    return json_response_object


def handle_intent(payload):
    # Get current context and intent
    context = context = payload['queryResult']['outputContexts'][0]['name'].split('/')[-1]
    intent = payload['queryResult']['intent']['displayName']
    user_response = (payload['queryResult']['queryText'])

    if intent == 'Ende':
        write_new_log()
        close_temp_log()

    if intent == 'Volkskontrolle':
        json_response_object = build_standard_response(message='Die Volkskontrolle wird gestartet. Hast du offene '
                                                               'Brut gesehen? ')
    elif intent == 'Neues Todo erfassen':
        json_response_object = build_standard_response(message='Alles klar, bitte nennen mir jetzt die neue Aufgabe.')
    elif intent == 'Letztes Todo abfragen':
        todo = db.session.query(Todos).order_by(Todos.id.desc()).first()
        json_response_object = build_standard_response(message='Hier deine letzte abgespeicherte Aufgabe: ' + todo.todo)
    elif context == 'todo':
        todo = Todos(todo=user_response)
        db.session.add(todo)
        db.session.commit()
        json_response_object = build_standard_response(message='Die neue Aufgabe wurde abgespeichert.')
    elif intent == 'Ja':
        json_response_object = handle_yes_no(payload, yes=True)
    elif intent == 'Nein':
        json_response_object = handle_yes_no(payload, yes=False)
    elif intent == 'Default Fallback Intent':
        json_response_object = \
            build_response_with_context(message='Das habe ich leider nicht verstanden',
                                        context=payload['queryResult']['outputContexts'][0]['name'])
    else:
        json_response_object = build_standard_response(message=payload['queryResult']['fulfillmentText'])

    return json_response_object


if __name__ == '__main__':
    app.run(debug=True)
