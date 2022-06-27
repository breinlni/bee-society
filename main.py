from flask import Flask, request, render_template
from handler import handle_yes_no
from utils import build_standard_response, build_response_with_context
from log_writer import write_new_log, write_temp_log, close_temp_log
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

working_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.sqlite3'
db = SQLAlchemy(app)


class Todos(db.Model):
    id = db.Column('ID', db.Integer, primary_key=True)
    todo = db.Column('Todo', db.String)

    def __init__(self, todo):
        self.todo = todo


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/', methods=['POST'])
def webhook():

    payload = request.json
    user_response = (payload['queryResult']['queryText'])
    bot_response = (payload['queryResult']['fulfillmentText'])
    print(f'User: {user_response}')
    print(f'Bot: {bot_response}')

    write_temp_log(f'User: {user_response}')
    write_temp_log(f'Bot: {bot_response}')

    context = context = payload['queryResult']['outputContexts'][0]['name'].split('/')[-1]

    if payload['queryResult']['intent']['displayName'] == 'Ende':
        write_new_log()
        close_temp_log()

    if payload['queryResult']['intent']['displayName'] == 'Volkskontrolle':
        json_response_object = build_standard_response(message='Die Volkskontrolle wird gestartet. Hast du offene '
                                                               'Brut gesehen? ')
    elif payload['queryResult']['intent']['displayName'] == 'Neues Todo erfassen':
        json_response_object = build_standard_response(message='Alles klar, bitte nennen mir jetzt die neue Aufgabe.')
    elif payload['queryResult']['intent']['displayName'] == 'Letztes Todo abfragen':
        todo = db.session.query(Todos).order_by(Todos.id.desc()).first()
        json_response_object = build_standard_response(message='Hier deine letzte abgespeicherte Aufgabe: ' + todo.todo)
    elif context == 'todo':
        todo = Todos(todo=user_response)
        db.session.add(todo)
        db.session.commit()
        json_response_object = build_standard_response(message='Die neue Aufgabe wurde abgespeichert.')
    elif payload['queryResult']['intent']['displayName'] == 'Ja':
        json_response_object = handle_yes_no(payload, yes=True)
    elif payload['queryResult']['intent']['displayName'] == 'Nein':
        json_response_object = handle_yes_no(payload, yes=False)
    elif payload['queryResult']['intent']['displayName'] == 'Default Fallback Intent':
        json_response_object = \
            build_response_with_context(message='Das habe ich leider nicht verstanden',
                                        context=payload['queryResult']['outputContexts'][0]['name'])
    else:
        json_response_object = build_standard_response(message=payload['queryResult']['fulfillmentText'])

    return json_response_object


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
