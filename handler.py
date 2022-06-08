from utils import build_response_with_event, build_error_response
from log_writer import write_new_log, close_temp_log


def handle_yes_no(payload, yes=True):
    context = payload['queryResult']['outputContexts'][0]['name'].split('/')[-1]
    if context == '__system_counters__':
        context = payload['queryResult']['outputContexts'][1]['name'].split('/')[-1]
    if context == 'volkskontrolle':
        event_name = 'koenigin-gesehen'
    elif context == 'koenigin-gesehen':
        event_name = 'waiselzellen-gesehen'
    elif context == 'waiselzellen-gesehen':
        if yes:
            event_name = 'waiselzellen-bestiftet'
        else:
            event_name = 'drohnenrahmen'
    elif context == 'waiselzellen-bestiftet':
        event_name = 'waiselzellen-gebrochen'
    elif context == 'waiselzellen-gebrochen':
        event_name = 'drohnenrahmen'
    elif context == 'drohnenrahmen':
        if yes:
            event_name = 'drohnenrahmen-ausschneiden'
        else:
            event_name = 'ende'
    elif context == 'drohnenrahmen-ausschneiden':
        event_name = 'ende'
    else:
        error_message = f'Error in function handle_yes_no: payload = {str(payload)}'
        write_new_log()
        close_temp_log()
        return build_error_response(error_message=error_message)

    response = build_response_with_event(event_name=event_name)

    return response
