from openai import OpenAI
import secrets

_client = None
        
def get_client():
    global _client
    if _client is None:
        _client = OpenAI(api_key=secrets.OPENAI_API_KEY)
    return _client
    