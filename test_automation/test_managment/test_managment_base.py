from typing import List


class test_managment_base_class():
    api = None
    statuses = {}

    def __init__(self):
        '''
            initialize api to the api wrapper object
            initialize statuses as a dictionary like {'untested': 3, 'passed': 1, 'failed': 5, 'blocked': 2, 'retest': 4, 'not_applicable': 6}
        '''
        raise NotImplementedError

    def add_result(self, **kwargs) -> List[dict]:
        '''
        must be implemented in the sub classes
        :param kwargs: request json dict for the add result method of the api
        :return: response json dict for the add result method of the api
        '''
        raise NotImplementedError

    def get_test_case(self, **kwargs):
        '''
        must be implemented in the sub classes
        :param kwargs: caseId
        :return: TestCase object created based on the test case definition in testmanagment implementation
        '''
        raise NotImplementedError

    def get_test_instance(self, **kwargs):
        '''
        must be implemented in the sub classes
        :param kwargs: caseId
        :return: TestCase object created based on the test case definition in testmanagment implementation
        '''
        raise NotImplementedError