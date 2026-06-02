import ollama

MODEL = "qwen2.5-coder:7b"

def main():
    print("Hello from python-react-pat!")

class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": self.system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        response = ollama.chat(model=MODEL, messages=self.messages)
        return response.message.content