from .ticker import TickerAgent

def return_zero(query):
    return 0

class FactualQA:

    def __init__(self):
        # high-level/general intent classifier
        self.intent_classifier = return_zero  # callable: query -> {0, 1, ..., n_intents}

        self.intent_id_to_name = {
            0: 'ticker',
            # ...
            # n: 'intent_n'
        }

        # intent agents
        self.intent_agents = {
            'ticker': TickerAgent(),  # class that implements an `answer` method
            # ...
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
        return agent.answer(query)
