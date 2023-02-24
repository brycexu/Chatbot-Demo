import re

class YearExtractor:

    def __init__(self):
        pass

    def __call__(self, query):
        '''
        Returns all occurrences of years in the `query`
        '''
        candidates = re.findall(r'\d+', query)
        candidates_clean = []
        for year in candidates:
            if year in ['2022','2021','2020','2019','2018']:
                candidates_clean.append(year)
        return candidates_clean
            
            
if __name__ == '__main__':
    extractor = YearExtractor()
    response = extractor('What is the forward eps of Tesla in 2019 and 2020?')
    print(response)
