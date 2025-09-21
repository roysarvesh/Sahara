# backend/dialogflow_client.py
import uuid
from google.cloud import dialogflowcx_v3beta1 as dialogflow
from google.api_core.exceptions import GoogleAPICallError, InvalidArgument

def detect_intent_text(project_id, location, agent_id, text, session_id=None, language_code="en"):
    if not session_id:
        session_id = str(uuid.uuid4())

    client_options = {"api_endpoint": f"{location}-dialogflow.googleapis.com"}
    session_client = dialogflow.SessionsClient(client_options=client_options)

    session_path = session_client.session_path(
        project=project_id, location=location, agent=agent_id, session=session_id
    )

    text_input = dialogflow.TextInput(text=text)
    query_input = dialogflow.QueryInput(text=text_input, language_code=language_code)
    request = dialogflow.DetectIntentRequest(session=session_path, query_input=query_input)
    try:
        response = session_client.detect_intent(request=request)
        response_messages = [
            " ".join(msg.text.text) for msg in response.query_result.response_messages if msg.text
        ]
        return "".join(response_messages), session_id
    except InvalidArgument as e:
        print(f"[Dialogflow ERROR] InvalidArgument: {e}")
        return "Dialogflow invalid request error.", session_id
    except GoogleAPICallError as e:
        print(f"[Dialogflow ERROR] API call failed: {e}")
        return "Dialogflow API connection error.", session_id
    except Exception as e:
        print(f"[Dialogflow ERROR] Unexpected exception: {e}")
        return "Dialogflow unknown error.", session_id
