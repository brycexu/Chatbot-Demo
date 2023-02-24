import re
import yfinance as yf
import numpy as np
import json
from qa_system.intent_agents.factual_qa.utils import query_model, get_company_name, SENTENCE_EMBEDDING_MODEL
from qa_system.intent_agents.factual_qa.utils import get_ticker_name

class TickerAgent:

    def __init__(self):
        self.back_up = self._get_local_ticker_infos()

    def _get_local_ticker_infos(self):
        ticker_path = "qa_system/constants/ticker_backup.json"
        with open(ticker_path, "r") as file:
            ticker_infos = json.load(file)
        return ticker_infos

    def get_ticker_info(self, company_name):
        tikername = get_ticker_name(company_name)
        try:
            ticker = dict(yf.Ticker(tikername).info)
        except:
            ticker = None
        return ticker, tikername

    def get_key(self, query, keys, company_name):
        sentences = []
        for key in keys:
            if key[-2:] == "PE":
                new_key = f'{key[:-2]} {key[-2:]}'
            else:
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
        if company_name is None:
            return "Unable to fetch company name", 0
        ticker_info, tikername = self.get_ticker_info(company_name)
        if ticker_info is None:
            if tikername in self.back_up:
                ticker_info = self.back_up[tikername]
            else:
                return f"Unable to fetch ticker information of {company_name}", 0
        key, sentence, score = self.get_key(query, list(ticker_info.keys()), company_name)
        answer = f"{sentence} is {ticker_info[key]}."
        return answer, ticker_info[key], score
