from .ticker import TickerAgent
from .ratio import RatioAgent
import re

def return_zero(query):
    candidates = re.findall(r'\d+', query)
    for year in candidates:
        if year in ['2022','2021','2020','2019','2018']:
            return 1
    return 0

class FactualQA:

    def __init__(self):
        # high-level/general intent classifier
        self.intent_classifier = return_zero  # callable: query -> {0, 1, ..., n_intents}

        self.intent_id_to_name = {
            0: 'ticker',
            1: 'ratio',
            # n: 'intent_n'
        }

        # intent agents
        self.intent_agents = {
            'ticker': TickerAgent(),  # class that implements an `answer` method
            'ratio': RatioAgent(),
            # 'intent_n': IntentNQA()
        }

    def _classify_intent(self, query):
        intent_id   = self.intent_classifier(query)      # {0, 1, ...}
        intent_name = self.intent_id_to_name[intent_id]  # {'ticker', ...}
        return intent_name

    def answer(self, query):
        # classify intent of query
        intent_name = self._classify_intent(query)

        # pass query to intent handler
        agent = self.intent_agents[intent_name]
        answer = agent.answer(query)

        return answer
