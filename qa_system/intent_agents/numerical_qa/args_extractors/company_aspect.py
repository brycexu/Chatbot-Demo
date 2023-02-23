import re

class ExactMatchCompanyAspectExtractor:

    def __init__(self):
        
        self.supported_entities_path = 'qa_system/constants/supported_company_aspects.txt'  # defined relative to root library dir

        self.entity_vbz_map = self._generate_verbalizations()
        # print(self.entity_vbz_map)

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

            if key[-2:] == "PE":
                new_key = f'{key[:-2]} {key[-2:]}'
            else:
                new_key = re.sub( r"([A-Z])", r" \1", key).split()
                new_key = " ".join(new_key)
                new_key = new_key.lower()
            verbalizations.append(new_key)

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


class CosineSimilarityCompanyAspectExtractor:

    def __init__(self):
        pass

    def _supported_company_aspects(self):
        '''
        Defines a map of {aspect_key: [verbalization1, verbalization2, ...]}
        used for exact-matching or cosine-similarity matching
        '''
        pass

    def __call__(self, query):
        '''
        Performs a maximum dot product similarity search between `query`
        and a pre-defined list of (possibly multiple verbalizations of)
        company aspects/properties.
        '''
        pass


if __name__ == '__main__':
    extractor = ExactMatchCompanyAspectExtractor()
    company_aspect = extractor('What is the forward eps of Tesla?')
    print(company_aspect)
