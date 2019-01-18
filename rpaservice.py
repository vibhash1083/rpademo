import dialogflow_v2 as dialogflow
import uuid
from flask import Flask, request
import os

session_id = uuid.uuid1()
project_id = "rpademo-e026c"
language_code = "en"

intent_map = {
    'Open browser': 'open_browser'
}

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def handle_message():
    '''
    Handle messages sent
    '''
    print("Message: ", request.get_json())
    texts = request.get_json()['texts']
    
    return detect_intent_texts(project_id, session_id, texts, language_code)


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    text_input = dialogflow.types.TextInput(
        text=texts, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    return response.query_result.fulfillment_text


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0', threaded=True)
