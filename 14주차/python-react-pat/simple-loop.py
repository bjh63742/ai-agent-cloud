import ollama
import re

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

action_re = re.compile('^Action: (\w+): (.*)$')   # python regular expression to selection action

def query(question, max_turns=5):
    i = 0
    bot = Agent(prompt)
    next_prompt = question
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        print("1:" + result)
        actions = []
        for a in result.split('\n'):
            m = action_re.match(a)
            if m:
                actions.append(m.groups())
        print("2: actions:", actions)
        if actions:
            # There is an action to run
            action, action_input = actions[0]
            print("3: -- action:", action, "input:", action_input)
            if action not in known_actions:
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print("4: -- running {} {}".format(action, action_input))
            observation = known_actions[action](action_input)
            print("Observation:", observation)
            next_prompt = "Observation: {}".format(observation)
        else:
            return
        

question = """나는 개를 2마리 키우고 있는데, border collie와 Scottish Terrier입니다. \
두 마리의 합산 체중은 얼마인가요?"""
query(question)