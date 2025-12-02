from openai import OpenAI
import config

class LLM:
    def __init__(self, client):
        print("[ LLM_SERVICE.PY ] Initializing LLM Service.")
        self.client = client

    def prompt(self, prompt: str):
        print("[ LLM_SERVICE.PY ] Prompting LLM...")
        try:
            response = self.client.responses.create(
                model=config.gpt_model,
                input=prompt
            )
            
            print("[ LLM_SERVICE.PY ] Received LLM response.")
            
            if hasattr(response, "output_text"):
                print(f"[ LLM_SERVICE.PY ] Sending response to Robot:          ' {response.output_text} '")
                return response.output_text
            
            if response.output and len(response.output) > 0:
                first_item = response.output[0]
                if hasattr(first_item, "content") and len(first_item.content) > 0:
                    print(f"[ LLM_SERVICE.PY ] Sending response to Robot:         ' {first_item.content[0].text} '")
                    return first_item.content[0].text
            
            raise RuntimeError("[ LLM_SERVICE.PY ] ERROR: Unexpected LLM response format.")
        
        except Exception as e:
            print(f"[ LLM_SERVICE.PY ] ERROR during prompt(): {e}")
            return ""