import requests
from urllib.request import urlopen
import certifi
import json

def get_ticker_name(company_name):
    '''
        :param company_name
        :return: ticker_name
        Ex: Amazon -> AMZN
    '''
    yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": company_name, "quotes_count": 1, "country": "United States"}

    res = requests.get(url=yfinance, params=params, headers={'User-Agent': user_agent})
    data = res.json()

    try:
        company_code = data['quotes'][0]['symbol']
    except:
        company_code = None
    return company_code



NER_MODEL = {"API_URL": "https://api-inference.huggingface.co/models/dslim/bert-base-NER-uncased",
             "headers": {"Authorization": "Bearer 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"}}
SENTENCE_EMBEDDING_MODEL = {
    "API_URL": "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2",
    "headers": {"Authorization": "Bearer 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"}}


def query_model(API_URL, headers, inputs):
    '''
        get huggingface model results from API_URL
    '''
    payload = {
        "inputs": inputs,
        "options": {"use_cache": True, "wait_for_model": True}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def get_company_name(query):
    tokens = query_model(NER_MODEL['API_URL'], NER_MODEL["headers"], query)
    company_name = None
    for token in tokens:
        if token['entity_group'] == 'ORG':
            company_name = token['word']
    return company_name

def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


