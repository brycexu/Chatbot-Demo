from .args_extractors import ExactMatchCompanyAspectExtractor, ExactMatchCompanyTickerExtractor, YearExtractor
from qa_system.intent_agents.factual_qa.factual_qa_agent import FactualQA
from qa_system.intent_agents.factual_qa.utils import get_key, get_company_name

import traceback


class PercentChangeAgent:


    def __init__(self):
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
        self.api_qa_system = None
        self.factual_qa_system = FactualQA().answer


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

        # company name
        company = get_company_name(query)

        # key
        aspect, _, _, aspect_readable = get_key(query, company)

        # years
        years_in_query = YearExtractor()(query)
        if len(years_in_query) > 2:
            raise NotImplementedError(f'Warning: more than 2 ({len(years_in_query)}) years mentioned in the query.')
        elif len(years_in_query) < 2:
            years_in_query = [None, None]

        args = {
            'aspect': aspect,
            'aspect_readable': aspect_readable,
            'company': company,
            'start_time': years_in_query[0],
            'end_time': years_in_query[1],
        }

        for k, v in args.items():
            if v is None:
                raise NotImplementedError(f'Warning: `{k}` in query "{query}" not recognized.')

        return args
    

    def _list_factual_qns(self, retrieval_type='FactualQA'):
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

            'api': {},  # not implemented

            'FactualQA': {
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
        }

        return factual_questions[retrieval_type]


    def _answer_factual_qns(self, factual_questions, retrieval_type='FactualQA'):
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
            
            if retrieval_type == 'api':
                answer = self.api_qa_system(qn)
            elif retrieval_type == 'FactualQA':
                answer, answer_num, score = self.factual_qa_system(qn)
            else:
                raise ValueError('Error: retrieval_type not recognized')
            
            factual_question_answer_pairs[qn_id] = {
                'answer_str': answer,
                'answer_num': answer_num,
                'score': score
            }

        return factual_question_answer_pairs

    
    def _calculate_answer(self, factual_qa_pairs):
        endval   = factual_qa_pairs['aspect_at_end']['answer_num']
        startval = factual_qa_pairs['aspect_at_start']['answer_num']
        return (endval - startval) / startval


    def answer(self, query):

        try:
            args = self._extract_args(query)
            self.args = args
            # print('[RatioAgent.answer] args:', args)

            factual_qns      = self._list_factual_qns()
            # print('[RatioAgent.answer] factual_qns', factual_qns)

            factual_qa_pairs = self._answer_factual_qns(factual_qns)
            # print('[RatioAgent.answer] factual_qa_pairs', factual_qa_pairs)

            numerical_answer = self._calculate_answer(factual_qa_pairs)
            # print('[RatioAgent.answer] numerical_answer', numerical_answer)

            # format evidences
            evidence_strs = [d['answer_str'] for d in factual_qa_pairs.values()]
            evidences_str = '\n'.join(evidence_strs)

            # format the final answer
            endval   = factual_qa_pairs['aspect_at_end']['answer_num']
            startval = factual_qa_pairs['aspect_at_start']['answer_num']
            answer_str = (
                f'So, the percentage change in '
                f'the {self.args["aspect_readable"]} '
                f'of {self.args["company"]} '
                f'between {self.args["start_time"]} '
                f'and {self.args["end_time"]} '
                f'is ({endval:.4f} - {startval:.4f}) / {startval:.4f}  = {numerical_answer:.4f}'
            )

            return f'{evidences_str}\n\n{answer_str}', numerical_answer, -1
        except NotImplementedError:
            return traceback.format_exc()



if __name__ == '__main__':
    agent  = PercentChangeAgent()
    answer = agent.answer('What is the percentage change in the debt-to-capital ratio of Amazon from 2008 to 2012?')
    print(answer)