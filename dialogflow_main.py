from flask import Flask, request, make_response
from handler import handle_yes_no
from utils import build_standard_response, build_response_with_context
from log_writer import write_new_log, write_temp_log, close_temp_log

app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    payload = request.json
    user_response = (payload['queryResult']['queryText'])
    bot_response = (payload['queryResult']['fulfillmentText'])
    print(f'User: {user_response}')
    print(f'Bot: {bot_response}')

    write_temp_log(f'User: {user_response}')
    write_temp_log(f'Bot: {bot_response}')

    if payload['queryResult']['intent']['displayName'] == 'Ende':
        write_new_log()
        close_temp_log()

    if payload['queryResult']['intent']['displayName'] == 'Volkskontrolle':
        json_response_object = build_standard_response(message='Die Volkskontrolle wird gestartet. Hast du offene '
                                                               'Brut gesehen? ')
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
    app.run(debug=True)
