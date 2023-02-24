# #################################
# How to use:
# Navigate to the directory which holds `qa.py` as your working directory.
# Modify the query in the main section of the bottom of this file.
# Run `python qa.py`
# #################################
import sys
sys.path.append("qa_system")

from intent_agents import FactualQA, NumericalQA
from intent_classifiers import RuleBasedIntentClassifier, NeuralIntentClassifier


def my_intent_classifier(query):
    return 0

class QA:

    '''
    A top-level wrapper that just handles routing queries to different intent handlers,
    e.g. 'factual', 'numerical', etc.

    Inside each agent, you should also handle intent classification if that is required
    within the agent.

    Design v1:
    1. Classify general intent using multiplexer ('factual' or 'numerical' or ...)
    2. Instantiate general intent answering agent ('factual' or 'numerical' or ...)
    3. Let the general intent answering agent handle the question, end-to-end

    '''

    def __init__(self):
        # high-level/general intent classifier
        # callable: query -> {0, 1, ..., n_intents}
        self.intent_classifier = RuleBasedIntentClassifier()

        # intent id to intent name: map {0, 1, ..., n_intents} -> {'factual', 'numerical', ... 'intent_n'}
        # move this to a common location later so that other parts of the QA shares a single source of truth
        self.intent_id_to_name = {
            0: 'factual',
            1: 'numerical',
            # ...
            # n: 'intent_n'
        }

        # intent agents
        self.intent_agents = {
            'factual': FactualQA(),  # class that implements an `answer` method
            'numerical': NumericalQA(),  # class that implements an `answer` method
            # ...
            # 'intent_n': IntentNQA()
        }

    def _classify_intent(self, query):
        intent_id   = self.intent_classifier(query)      # {0, 1, ...}
        if intent_id == -1:
            return None
        intent_name = self.intent_id_to_name[intent_id]  # {'factual', 'numerical', ...}
        return intent_name


    def answer(self, query):
        # classify intent of query
        intent_name = self._classify_intent(query)

        if not intent_name:
            return "We are currently unable to answer this category of question."

        # pass query to intent handler
        agent = self.intent_agents[intent_name]
        try:
            response, response_numerical, score = agent.answer(query)
        except:
            return "We are currently unable to answer this category of question."
        return response

if __name__ == '__main__':
    qa = QA()
    # response = qa.answer('What is the debt ratio of Tesla?')
    response = qa.answer('What is the quick ratio of Amazon in 2020?')