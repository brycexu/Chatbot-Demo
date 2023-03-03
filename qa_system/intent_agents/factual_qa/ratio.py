from qa_system.intent_agents.factual_qa.utils import query_model, get_company_name, SENTENCE_EMBEDDING_MODEL
from qa_system.intent_agents.factual_qa.utils import get_ticker_name, get_jsonparsed_data
import numpy as np
import re

class RatioAgent:
    def __init__(self):
        pass

    def get_year(self, query):
        candidates = re.findall(r'\d+', query)
        for year in candidates:
            if year in ['2022','2021','2020','2019','2018']:
                return year

    def get_ratio_info(self, ticker_name, year):
        url = (f"https://financialmodelingprep.com/api/v3/ratios/{ticker_name}?apikey=b189c503fb8f71a8c931cf1c660105d6")
        data = get_jsonparsed_data(url)
        for info in data:
            if year in info['date']:
                del info['symbol']
                del info['date']
                del info['period']
                return info

    def get_key(self, query, keys, company_name):
        sentences = []
        for key in keys:
            new_key = re.sub(r"([A-Z])", r" \1", key).split()
            new_key = " ".join(new_key)
            new_key = re.sub(r"_", r" ", new_key)
            new_key = new_key.lower()
            sentences.append('The ' + new_key + ' of ' + company_name)

        inputs = {
            "source_sentence": query,
            "sentences": sentences
        }
        scores = query_model(SENTENCE_EMBEDDING_MODEL["API_URL"], SENTENCE_EMBEDDING_MODEL["headers"], inputs)
        idx = np.argmax(scores)
        return keys[idx], sentences[idx], scores[idx]

    def answer(self, query):
        company_name = get_company_name(query)
        ticker_name = get_ticker_name(company_name)
        if not ticker_name:
            return f"Unable to fetch ticker name", None, 0
        year = self.get_year(query)
        if not year:
            return f"Please provide a year between [2018, 2022]", None, 0
        ratio_info = self.get_ratio_info(ticker_name, year)
        key, sentence, score = self.get_key(query, list(ratio_info.keys()), company_name)
        value = ratio_info[key]
        value = round(value, 4) if type(value) in [int, float] else value
        answer = f"{sentence} is {value} in {year}."
        return answer, ratio_info[key], score  # answer in sentence form, numerical answer, confidence

