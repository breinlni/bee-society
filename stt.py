import io
import os
from datetime import datetime
from google.cloud import dialogflow, speech


def detect_intent_audio(audio_file_path, project_id='beesociety-qjhf', language_code='de', session_id=None):
    """Returns the result of detect intent with an audio file as input.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    """if session_id is None:
        session_id = datetime.now().strftime("%d%m%Y%H%M%S")"""

    session_client = dialogflow.SessionsClient()

    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    audio_encoding = speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
    sample_rate_hertz = 48000

    session_id = 'Test123'
    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    with open(audio_file_path, "rb") as audio_file:
        input_audio = audio_file.read()

    audio_config = dialogflow.InputAudioConfig(
        audio_encoding=audio_encoding,
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
    )
    query_input = dialogflow.QueryInput(audio_config=audio_config)

    request = dialogflow.DetectIntentRequest(session=session, query_input=query_input, input_audio=input_audio)
    response = session_client.detect_intent(request=request)

    print("=" * 20)
    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))

    """context = response.query_result.output_contexts[0].name.split('/')[-1]
    if context == '__system_counters__':
        context = response.query_result.output_contexts[1].name.split('/')[-1]

    print(f'Context: {context}')"""

    return response.query_result.intent.display_name


def detect_intent_texts(texts, project_id='beesociety-qjhf', session_id=None, language_code='de'):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))


def speech_to_text(audio_file):
    client = speech.SpeechClient()

    # Full path of the audio file, Replace with your file name
    file_name = os.path.join(os.path.dirname(__file__), audio_file)

    # Loads the audio file into memory
    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        audio_channel_count=1,
        language_code="de",
    )

    # Sends the request to google to transcribe the audio
    response = client.recognize(request={"config": config, "audio": audio})

    # Reads the response
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

