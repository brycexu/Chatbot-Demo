from .percent_change import PercentChangeAgent
from .ratio import RatioAgent

def return_zero(query):
    return 1

class NumericalQA:

    '''
    Routes the query to the correct handler, similar to how the high-level QA system
    routes requests to the different intent agents.

    Might be a good idea to inherit from the QA class.
    '''

    def __init__(self):

        # high-level/general intent classifier
        self.intent_classifier = return_zero  # callable: query -> {0, 1, ..., n_intents}

        # intent id to intent name: map {0, 1, ..., n_intents} -> {'factual', 'numerical', ... 'intent_n'}
        # move this to a common location later so that other parts of the QA shares a single source of truth
        self.intent_id_to_name = {
            0: 'ratio',
            1: 'percent_change',
            # ...
            # n: 'intent_n'
        }

        # intent agents
        self.intent_agents = {
            'ratio': RatioAgent(),  # class that implements an `answer` method
            'percent_change': PercentChangeAgent(),
            # ...
            # 'intent_n': IntentNQA()
        }
        

    def _classify_intent(self, query):
        intent_id   = self.intent_classifier(query)      # {0, 1, ...}
        intent_name = self.intent_id_to_name[intent_id]  # {'factual', 'numerical', ...}
        return intent_name


    def answer(self, query):
        # classify intent of query
        intent_name = self._classify_intent(query)

        # pass query to intent handler
        agent = self.intent_agents[intent_name]
        return agent.answer(query)