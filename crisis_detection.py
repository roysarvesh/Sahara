# backend/crisis_detection.py
import re

CRISIS_KEYWORDS = {
    "suicide": ["kill myself", "want to die", "end my life", "suicidal"],
    "self_harm": ["hurt myself", "cutting", "self harm", "burn myself"],
    "abuse": ["abused", "being hit", "domestic violence", "raped"],
    "severe_distress": ["can't go on", "can't take it anymore", "hopeless"]
}

CRISIS_RESPONSE_MESSAGE = (
    "It sounds like you are going through a very difficult time. It's important to talk to someone who can help right now. "
    "Please reach out to one of these 24/7 free and confidential helplines in India:\n\n"
    "- **Tele MANAS**: Call 14416\n"
    "- **Vandrevala Foundation**: Call +91 9999 666 555\n"
    "- **Aasra**: Call +91 9820466726\n\n"
    "Your safety is the most important thing. Please reach out for help."
)

def is_crisis_message(message: str) -> tuple[bool, str | None]:
    """
    Detects crisis signals and returns a tuple of (is_crisis, response_message).
    If it is a crisis, the response message is returned. Otherwise, it's None.
    """
    lower_message = message.lower()
    for crisis_type, keywords in CRISIS_KEYWORDS.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', lower_message):
                print(f"CRISIS DETECTED: Type '{crisis_type}' based on keyword '{keyword}'.")
                return True, CRISIS_RESPONSE_MESSAGE
    return False, None
