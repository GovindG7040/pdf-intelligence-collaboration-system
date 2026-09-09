from langchain_ollama import ChatOllama


class OllamaService:
    """
    Creates and manages the Ollama Large Language Model.
    """

    def __init__(self, model_name: str = "gemma3:4b", temperature: float = 0.2,):

        self.llm = ChatOllama(
            model=model_name,
            temperature=temperature,
        )

        print(f"Ollama model '{model_name}' loaded successfully.")

    # =====================================================
    # RETURN LLM
    # =====================================================

    def get_llm(self):

        return self.llm