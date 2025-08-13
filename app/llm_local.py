import subprocess

class OllamaLLM:
    """
    Minimal wrapper for a local Ollama model.
    Requires: https://ollama.com/ and a model like `llama3.1` or `qwen2.5:3b-instruct`.

    Usage:
        llm = OllamaLLM(model="llama3.1")
        text = llm.chat("Say hi")
    """
    def __init__(self, model: str = "llama3.1"):
        self.model = model

    def chat(self, prompt: str) -> str:
        try:
            proc = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            out = proc.stdout.decode("utf-8", errors="ignore").strip()
            err = proc.stderr.decode("utf-8", errors="ignore").strip()
            if err and not out:
                return f"[Ollama error] {err}"
            return out if out else "[No response from local model]"
        except FileNotFoundError:
            return (
                "Ollama not found. Install from https://ollama.com/ and run `ollama run llama3.1` once to download."
            )
