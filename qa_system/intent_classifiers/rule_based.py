from qa_system.intent_agents import FactualQA, NumericalQA

class RuleBasedIntentClassifier:

    def __init__(self):
        self.factual_keywords_path = "questions/factual_keyword.txt"
        self.factual_keywords = set()
        with open(self.factual_keywords_path, "r") as in_file:
            lines = in_file.readlines()
            for line in lines:
                self.factual_keywords.add(line[:-1])
        self.numerical_keywords_path = "questions/numerical_keyword.txt"
        self.numerical_keywords = set()
        with open(self.numerical_keywords_path, "r") as in_file:
            lines = in_file.readlines()
            for line in lines:
                self.numerical_keywords.add(line[:-1])

    def __call__(self, query):
        query = query.lower()
        for factual_keyword in self.factual_keywords:
            if "the " + factual_keyword.lower() in query:
                return 0
        for numerical_keyword in self.numerical_keywords:
            if "the " + numerical_keyword.lower() in query:
                return 1
        return -1
