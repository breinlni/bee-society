

def build_response_with_event(event_name):
    json_response_object = {
        "fulfillmentMessages": [{
            "text": {
                "text": ['test']
            }
        }],
        "followupEventInput": {
            "name": event_name,
            "languageCode": "de"
        }
    }
    return json_response_object


def build_error_response(error_message):
    json_response_object = {
        "fulfillmentMessages": [{
            "text": {
                "text": [error_message]
            }
        }]
    }
    return json_response_object


def build_standard_response(message):
    json_response_object = {
        "fulfillmentMessages": [{
            "text": {
                "text": [message]
            }
        }]
    }
    return json_response_object


def build_response_with_context(message, context):
    json_response_object = {
        "fulfillmentMessages": [{
            "text": {
                "text": [message]
            }
        }],
        "outputContexts": [
            {
                "name": context,
                "lifespanCount": 1,
            }
        ]
    }
    return json_response_object

