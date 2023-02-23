import requests

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


NER_MODEL = {"API_URL": "https://api-inference.huggingface.co/models/dslim/bert-base-NER",
             "headers": {"Authorization": "Bearer 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"}}
SENTENCE_EMBEDDING_MODEL = {"API_URL": "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2",
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

