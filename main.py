# backend/main.py (Version 2.0 for debugging)

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import logging
from dotenv import load_dotenv

from crisis_detection import is_crisis_message
from dialogflow_client import detect_intent_text

load_dotenv()

SHOW_DEBUG = os.getenv("SHOW_DEBUG", "true").lower() in ("1", "true", "yes")

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

chat_history = {}
DEFAULT_GREETING = "Hello! I'm Sahara, your AI companion. I'm here to listen and support you in a safe, non-judgmental space. How are you feeling today?"

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Sahara backend is running!", "version": "2.0"}), 200

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True) or {}
        user_message = data.get("message") or data.get("text") or ""
        session_id = data.get("sessionId") or data.get("session_id")
        
        if not session_id:
            session_id = str(uuid.uuid4())
            logging.info(f"Created new session_id: {session_id}")

        if session_id not in chat_history:
            chat_history[session_id] = []
            if not user_message.strip():
                return jsonify({
                    "reply": DEFAULT_GREETING,
                    "session_id": session_id,
                    "isCrisis": False,
                    "history": [{"role": "bot", "message": DEFAULT_GREETING}],
                    "version": "2.0"
                }), 200
            chat_history[session_id].append({"role": "bot", "message": DEFAULT_GREETING})

        if not user_message.strip():
            return jsonify({
                "reply": chat_history[session_id][-1].get("message", "How can I help?"),
                "session_id": session_id,
                "isCrisis": False,
                "history": chat_history[session_id],
                "version": "2.0"
            }), 200

        chat_history[session_id].append({"role": "user", "message": user_message})

        is_crisis, crisis_response = is_crisis_message(user_message)
        if is_crisis:
            bot_reply = crisis_response
        else:
            project_id = os.getenv("GCP_PROJECT_ID")
            location = os.getenv("DF_LOCATION") or "global"
            agent_id = os.getenv("DF_AGENT_ID")

            if not (project_id and agent_id):
                msg = "Dialogflow configuration missing (GCP_PROJECT_ID or DF_AGENT_ID)."
                logging.error(msg)
                raise RuntimeError(msg)

            df_response_text, _ = detect_intent_text(
                project_id=project_id,
                location=location,
                agent_id=agent_id,
                text=user_message,
                session_id=session_id,
                language_code=data.get("language_code", "en")
            )
            bot_reply = df_response_text or "Sorry, I didn't understand that."

        chat_history[session_id].append({"role": "bot", "message": bot_reply})

        return jsonify({
            "reply": bot_reply,
            "session_id": session_id,
            "isCrisis": is_crisis,
            "history": chat_history[session_id],
            "version": "2.0"
        }), 200

    except Exception as e:
        logging.exception("Exception in /chat route")
        response_payload = {
            "reply": "I'm sorry, something went wrong. Please try again.",
            "isCrisis": False,
            "version": "2.0"
        }
        if SHOW_DEBUG:
            response_payload["debug"] = str(e)
        return jsonify(response_payload), 500

@app.route("/history/<session_id>", methods=["GET"])
def get_history(session_id):
    if session_id not in chat_history:
        return jsonify({"error": "Session not found", "session_id": session_id}), 404
    return jsonify({
        "session_id": session_id,
        "history": chat_history[session_id]
    }), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
