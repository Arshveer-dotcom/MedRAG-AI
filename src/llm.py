from typing import Optional


class MedicalLLM:
    """Handles LLM interactions via Ollama or OpenAI."""

    def __init__(self, model_name: str = "llama3.2:3b", base_url: str = "http://localhost:11434",
                 openai_api_key: str = "", openai_model: str = "gpt-4o-mini"):
        self.model_name = model_name
        self.base_url = base_url
        self.use_openai = bool(openai_api_key)
        self.backend = None

        if self.use_openai:
            print(f"Initializing OpenAI LLM: {openai_model}")
            try:
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    model=openai_model,
                    api_key=openai_api_key,
                    temperature=0.3,
                    timeout=120,
                )
                self.backend = "openai"
                print(f"Successfully initialized OpenAI: {openai_model}")
            except Exception as e:
                print(f"Error initializing OpenAI: {e}")
                raise
        else:
            print(f"Initializing Ollama LLM: {model_name}")
            print(f"Ollama server: {base_url}")
            try:
                from langchain_ollama import OllamaLLM
                self.llm = OllamaLLM(
                    model=model_name,
                    base_url=base_url,
                    temperature=0.3,
                    num_ctx=4096,
                    timeout=120,
                )
                self.backend = "ollama"
                print(f"Successfully initialized Ollama: {model_name}")
            except Exception as e:
                print(f"Error initializing Ollama: {e}")
                raise

    def generate_medical_answer(self, context: str, question: str) -> str:
        prompt = f"""You are a medical information assistant. Answer the user's question based ONLY on the provided medical context.

IMPORTANT RULES:
1. Answer ONLY based on the provided context
2. If the context doesn't contain enough information, say "I could not find this information in the available medical knowledge base."
3. Do NOT make up or hallucinate medical information
4. Always remind the user that this is for educational purposes only
5. For medical concerns, always recommend consulting a healthcare professional

Medical Context:
{context}

User Question: {question}

Answer:"""

        try:
            response = self.llm.invoke(prompt)
            if hasattr(response, "content"):
                return response.content.strip()
            return str(response).strip()
        except Exception as e:
            err = str(e)
            if "Cannot assign requested address" in err or "Errno 99" in err:
                return "Could not connect to Ollama. Make sure Ollama is running (`ollama serve`) and accessible at the configured URL."
            if "Connection refused" in err:
                return "Ollama connection refused. Start Ollama with `ollama serve` and ensure it's listening on the correct port."
            if "openai" in err.lower() or "api_key" in err.lower():
                return f"OpenAI API error: {err}. Check your OPENAI_API_KEY."
            return f"Error generating response: {err}"

    def test_connection(self) -> bool:
        try:
            self.llm.invoke("Hello, this is a test.")
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
