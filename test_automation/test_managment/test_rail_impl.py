from typing import List

from testrail_api import TestRailAPI

from test_automation.data_objects.test_case import TestCase
from test_automation.data_objects.test_instance import TestInstance
from test_automation.test_managment.test_managment_base import test_managment_base_class


class test_rail(test_managment_base_class):
    def __init__(self, base_url: str, user_name: str, password: str):
        '''
            initializing TestRail API based on the input arguments then fetching the statuses using the api
        :param base_url: base url for the api
        :param user_name: user name
        :param password: password
        '''
        self.api = TestRailAPI(base_url, user_name, password)
        self.statuses = {'untested': 3, 'passed': 1, 'failed': 5, 'blocked': 2, 'retest': 4, 'not_applicable': 6}
        # for s in self.api.statuses.get_statuses():
        #     statuses_dict[s.get('name').lower()] = s.get('id')
        # self.statuses = statuses_dict

    def add_result(self, status: str, defects=None, comments: str = '', test_id: int = -1,
                   run_id: int = -1, case_id: int = -1, elapsed: str = '', attachments: list = None) -> dict:
        if defects is None:
            defects = set()
        result = None
        defect_str = set()
        for d in defects:
            defect_str.add(d.defectId)
        if test_id > 0:
            result = self.api.results.add_result(test_id=test_id, status_id=self.statuses[status],
                                                 defects=','.join(defect_str), comment=comments, elapsed=elapsed)
            result_id = result.get('id')
            print(defects)
            print(defect_str)

        else:
            result = self.api.results.add_result_for_case(run_id=run_id, case_id=case_id,
                                                          status_id=self.statuses[status],
                                                          defects=', '.join(defect_str), comment=comments,
                                                          elapsed=elapsed)
            print(defects)
            print(defect_str)
            result_id = result.get('id')
        if attachments:
            for a in attachments:
                self.add_attachment(result_id, a)
        return result

    def get_test_case(self, caseId: int) -> TestCase:
        return TestCase(self.api.cases.get_case(caseId))

    def get_test_instance(self, testId: int) -> TestInstance:
        return TestInstance(self.api.tests.get_test(testId))

    def add_attachment(self, result_id: int, path):
        return self.api.attachments.add_attachment_to_result(result_id, path)
