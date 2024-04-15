from imports import *

class LLMMetadata:
    def __init__(self, model_name, api_key, context_window=4096, num_output=256, is_chat_model=False):
        self.model_name = model_name
        self.api_key = api_key
        self.context_window = context_window
        self.num_output = num_output
        self.is_chat_model = is_chat_model  # Add this line

class HuggingFaceAPIAdapter(CustomLLM):
    @staticmethod
    def query_hf_api(model_name: str, api_key: str, prompt: str, context=None, **kwargs: Any) -> str:
        """Query the Hugging Face API and return the response text."""
        api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        headers = {"Authorization": f"Bearer {api_key}"}

        full_prompt = f"{context}\n{prompt}" if context else prompt  # Prepend context to the prompt if it exists

        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": kwargs.get("max_new_tokens", 1000),
                "return_full_text": False
            }
        }
        response = requests.post(api_url, headers=headers, json=payload)

        # Check if the response is a list and extract the first element if so
        if isinstance(response.json(), list):
            data = response.json()[0]  # Assuming you want the first result
        else:
            data = response.json()

        # Extract "generated_text" from the response
        if isinstance(data, dict):
            return data.get("generated_text", "")
        else:
            return ""  # Return an empty string or handle as needed

    @llm_completion_callback()
    def complete(self, prompt: str, formatted: bool = False, **kwargs: Any) -> CompletionResponse:
        # Static configuration within the method. Adjust as needed.
        model_name = "google/gemma-7b"
        api_key = "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"
        text_response = HuggingFaceAPIAdapter.query_hf_api(model_name, api_key, prompt, **kwargs)
        return CompletionResponse(text=text_response)

    @llm_completion_callback()
    def stream_complete(self, prompt: str, formatted: bool = False, **kwargs: Any) -> CompletionResponse:
        # This example doesn't implement real streaming; adjust according to your requirements.
        model_name = "google/gemma-7b"
        api_key = "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"
        text_response = HuggingFaceAPIAdapter.query_hf_api(model_name, api_key, prompt, **kwargs)
        for char in text_response:
            yield CompletionResponse(text=char, delta=char)

    # If your base class or framework expects a metadata method or property, provide a stub or actual implementation
    @property
    def metadata(self):
        # Return an instance of LLMMetadata with the required details
        return LLMMetadata(model_name="google/gemma-7b", api_key="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")
