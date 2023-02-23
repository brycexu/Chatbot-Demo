import re


class ExactMatchCompanyTickerExtractor:

    def __init__(self):
        
        self.supported_entities_path = 'qa_system/constants/supported_company_tickers.txt'  # defined relative to root library dir

        self.entity_vbz_map = self._generate_verbalizations()
        # print(self.aspect_vbz_map)

    def _generate_verbalizations(self):
        '''
        Defines a map of {aspect_key: [verbalization1, verbalization2, ...]}
        used for exact-matching or cosine-similarity matching
        '''

        # read
        with open(self.supported_entities_path, 'r') as f:
            aspect_list = f.read().splitlines()

        # map each key to some verbalizations
        # the example below maps "firstKeyName" -> ["first key name"]
        entity_verbalization_map = {}
        for key in aspect_list:

            verbalizations = []

            if key == 'TSLA':
                verbalizations = ['Tesla']
            elif key == 'AMZN':
                verbalizations = ['Amazon']

            entity_verbalization_map[key] = verbalizations

        return entity_verbalization_map


    def __call__(self, query):
        '''
        Searches for an exact match between substrings in `query` and `aspect_vbz_map`.
        Returns the first match. If no match found, returns None.
        '''
        key_match = None
        for key, vbz_list in self.entity_vbz_map.items():

            if key_match is not None:
                break

            for vbz in vbz_list:
                if vbz in query:
                    key_match = key
                    break

        return key_match

