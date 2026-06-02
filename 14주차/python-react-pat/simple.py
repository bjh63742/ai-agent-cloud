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
    

prompt = """
당신은 생각(Thought), 행동(Action), 일시정지(PAUSE), 관찰(Observation)의 반복 루프로 실행됩니다.
루프의 마지막에는 답변(Answer)을 출력합니다.
생각(Thought)은 질문에 대한 당신의 사고 과정을 설명하는 데 사용합니다.
행동(Action)은 사용 가능한 행동 중 하나를 실행하는 데 사용하며, 이후 일시정지(PAUSE)를 반환합니다.
관찰(Observation)은 해당 행동을 실행한 결과입니다.

사용 가능한 행동:

calculate:
예시: calculate: 4 * 7 / 3
계산을 수행하고 숫자를 반환합니다 - Python을 사용하므로 필요한 경우 반드시 부동소수점 문법을 사용하세요

average_dog_weight:
예시: average_dog_weight: Collie
견종이 주어지면 해당 개의 평균 체중을 반환합니다

예시 세션:

Question: 불독의 체중은 얼마인가요?
Thought: average_dog_weight를 사용하여 개의 체중을 조회해야겠다
Action: average_dog_weight: Bulldog
PAUSE

그러면 다음과 함께 다시 호출됩니다:

Observation: 불독의 체중은 51 lbs입니다

그 후 다음을 출력합니다:

Answer: 불독의 체중은 51 lbs입니다
""".strip()

def calculate(what):
    return eval(what)

def average_dog_weight(name):
    if name in "Scottish Terrier": 
        return("Scottish Terriers average 20 lbs")
    elif name in "Border Collie":
        return("a Border Collies average weight is 37 lbs")
    elif name in "Toy Poodle":
        return("a toy poodles average weight is 7 lbs")
    else:
        return("An average dog weights 50 lbs")

known_actions = {
    "calculate": calculate,
    "average_dog_weight": average_dog_weight
}

abot = Agent(prompt)

result = abot("Toy Poodle의 체중은 얼마인가요?")
print("1:" + result)

result = average_dog_weight("Toy Poodle")
print("2:" + result)

next_prompt = "Observation: {}".format(result)

print(next_prompt)
result = abot(next_prompt)
print("3:" + result)