from .args_extractors import ExactMatchCompanyAspectExtractor, ExactMatchCompanyTickerExtractor
import traceback

class PercentChangeAgent:


    def __init__(self, demo:bool = False):
        '''
        Typical question answered by this agent: 
            "what is the percentage change "
            "in the <aspect> "
            "of <company> "
            "from <start_time> to <end_time>?"

        Params:
        - demo: instantiate with synthetic data for demonstrations
        '''

        # callable that answers factual questions
        self.factual_qa_system = None

        self.demo = demo


    def _extract_args(self, query:str):
        '''
        Detects arguments/payload from user's query, saves into `self.args`.
        
        Example format:
        return {
            'aspect': 'debt-to-capital ratio',
            'company': 'Amazon',
            'start_time': '2008',
            'end_time': '2012'
        }
        '''
        return {}
    

    def _list_factual_qns(self):
        '''
        Given the extracted arguments, lists the factual questions it needs to ask
        from the factual QA system, an external API such as yfinance or finnhub, etc.

        TODO: decide if use QA or deterministic API
        QA pros: 
            deals with variation in user query; no need to map self.args.keys
            to data source's keys, which may be difficult to do in the answering agent
        API pros:
            less complex; no need to load/call a huge QA system

        This example uses the QA approach.
        '''

        args = self.args

        # list of factual questions that need to be answered to answer the question
        factual_questions = {

            # <aspect> of <company> at <start_time>
            'aspect_at_start': (  # aspect_at_start is a generic identifier of the fact
                f'What is the {args["aspect"]} '
                f'of {args["company"]} '
                f'in {args["start_time"]}?'
            ),

            # <aspect> of <company> at <end_time>
            'aspect_at_end': (
                f'What is the {args["aspect"]} '
                f'of {args["company"]} '
                f'in {args["end_time"]}?'
            ),
        }

        return factual_questions


    def _answer_factual_qns(self, factual_questions):
        '''
        Given the questions determined in `factual_questions`, call the QA system
        or the external API to answer the questions.

        Params:
        - factual_questions: list of factual questions whose answers are necessary
          to answer the user's query

        TODO: decide if use QA or deterministic API.
        This example uses the QA approach.
        '''

        # saves answers here
        factual_question_answer_pairs = {}
        
        # request the answer to each question from the factual QA system
        for qn_id, qn in factual_questions.items():
            
            answer = self.factual_qa_system(qn)
            factual_questions[qn_id] = answer

        return factual_question_answer_pairs

    
    def _calculate_answer(self, factual_qa_pairs):
        return (factual_qa_pairs['aspect_at_end'] - factual_qa_pairs['aspect_at_start']) / factual_qa_pairs['aspect_at_start']


    def answer(self, query):

        try:
            args = self._extract_args(query)
            self.args = args
            # print('args:', args)
        except NotImplementedError:
            return traceback.format_exc()

        factual_qns      = self._list_factual_qns()
        factual_qa_pairs = self._answer_factual_qns(factual_qns)
        numerical_answer = self._calculate_answer(factual_qa_pairs)

        return f'{query} is {numerical_answer:.3f}'


if __name__ == '__main__':
    agent  = PercentChangeAgent()
    answer = agent.answer('What is the percentage change in the debt-to-capital ratio of Amazon from 2008 to 2012?')
    print(answer)