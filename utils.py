import json

def safe_json_loads(response_text):
    try:
        return json.loads(response_text)
    except:
        # fallback cleanup
        cleaned = response_text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned)


def normalize_score(value):
    try:
        value = int(value)
        return max(0, min(100, value))
    except:
        return 0