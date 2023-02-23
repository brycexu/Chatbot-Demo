from .args_extractors import (
    ExactMatchCompanyTickerExtractor, 
    ExactMatchRatioNameExtractor
)
import yfinance as yf
import traceback


def yfinance_qa(args_dict):
    ticker_info = yf.Ticker(args_dict['company']).info
    ticker_info = dict(ticker_info)
    print('[yfinance_qa] ticker_info:', ticker_info)
    return ticker_info.get(args_dict['key'], None)


class RatioAgent:


    def __init__(self):
        '''
        Typical question answered by this agent: 
            "what is the <ratio_name> ratio "
            "of <company>?"

        TODO: map each <ratio_name> to a (ratio_num, ratio_denom)
        '''

        # callable that answers factual questions
        self.api_qa_system = yfinance_qa
        self.factual_qa_system = None


    def _extract_args(self, query:str):
        '''
        Detects arguments/payload from user's query, saves into `self.args`.
        
        Example format:
        return {
            'ratio_name': 'debtRatio',
            'company': 'Amazon',
        }
        '''
        args = {
            'ratio_name': ExactMatchRatioNameExtractor()(query),
            'company': ExactMatchCompanyTickerExtractor()(query)
        }

        for k, v in args.items():
            if v is None:
                raise NotImplementedError(f'Warning: `{k}` in query "{query}" not recognized.')

        return args
        

    def _list_factual_qns(self, retrieval_type='api'):
        '''
        Maps each `ratio_name` to a list of factual questions, in two formats:
        1. To call an API, e.g. yfinance: stores the keys used to index yfinance correctly
        2. To call the FactualQA system: stores a natural language query

        Params:
        1. retrieval_type: whether to use the `api` or `FactualQA` method of answering
           factual questions.
        '''

        args = self.args

        all_ratios = {
            
            # debt ratio: totalDebt/totalAssets
            'debtRatio': {
                'api': {
                    'num': {
                        'aspect': 'totalDebt',
                        'company': args['company']
                    },
                    'denom': {
                        'aspect': 'totalAssets',
                        'company': args['company']
                    }
                },

                'FactualQA': {
                    'num': (
                        f'What is the total debt '
                        f'of {args["company"]}?'
                    ),
                    'denom': (
                        f'What is the total assets '
                        f'of {args["company"]}?'
                    ),
                }
            }
        }
        
        ratio_name = args.get('ratio_name', None)
        if ratio_name is None:
            raise ValueError('Error: ratio_name is None. Please check argument extractor.')
        elif ratio_name in all_ratios.keys():
            return all_ratios[ratio_name][retrieval_type]
        else:
            raise NotImplementedError(f'Warning: `{ratio_name}` not recognized.')


    def _answer_factual_qns(self, factual_questions, retrieval_type='api'):
        '''
        Given the questions determined in `factual_questions`, call the QA system
        or the external API to answer the questions.

        Params:
        - factual_questions: list of factual questions whose answers are necessary
          to answer the user's query

        TODO: decide if use QA or deterministic API.
        This example uses the API approach.
        '''

        # saves answers here
        factual_question_answer_pairs = {}
        
        # request the answer to each question from the factual QA system
        for qn_id, qn in factual_questions.items():
            
            if retrieval_type == 'api':
                answer = self.api_qa_system(qn)
            elif retrieval_type == 'FactualQA':
                answer = self.factual_qa_system(qn)
            else:
                raise ValueError('Error: retrieval_type not recognized')
            
            factual_questions[qn_id] = answer

        return factual_question_answer_pairs

    
    def _calculate_answer(self, factual_qa_pairs):
        return factual_qa_pairs['num'] / factual_qa_pairs['denom']


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

            return f'{self.args["ratio_name"]} of {self.args["company"]} is {numerical_answer:.3f}'
        except NotImplementedError:
            return traceback.format_exc()
        

