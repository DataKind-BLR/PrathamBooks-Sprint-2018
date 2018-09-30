'''
A script to evaluate the tags with the test set.

We want to avoid doing exact matches for tags, as the tags generated might be similar
So we are extending the valid tags list by, idea taken from http://www.aclweb.org/anthology/R09-1086:-
    1. Exact matches
    2. Include Matches
    3. Part of Matches
    4. Lemmatization

This list can be extended more and by default all the matches are of equal weights.
'''

class EvalFunction(object):
    '''
    Eval Base Class.

    Extend this class to add more evaluation function.
    '''

    def __init__(self):
        return

    def pre_process(self, keywords):
        '''
        Extend this function to add pre processing for the keywords
        '''
        return keywords

    def eval(self, keywords, pred_keywords):
        '''
        Extend this function to add evaluation logic
        '''
        raise NotImplementedError("This is not implemented in the base class")


class ExactEvalFunction(EvalFunction):
    '''
    Eval Function to do exact matching of the keywords
    '''

    def pre_process(keywords):
        '''
        Basic processing, lower the keywords
        '''
        return [word.lower() for word in keywords]

    def eval(self, keywords, pred_keywords):
        '''
        Do a set intersection and return the number of common words for each row.
        '''
        keywords = [self.pre_process(kwrds) for kwrds in keywords]
        return [len(set(a).intersection(set(b))) for a, b in keywords, pred_keywords]
