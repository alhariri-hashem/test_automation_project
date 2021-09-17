import argparse
from pathlib import Path

import PIL.Image

from test_automation.Utils.exploratory_testing_cli import ExploratoryTestingMenu
from test_automation.data_objects.defect import Defect
from test_automation.data_objects.test_case import TestCase
from test_automation.data_objects.test_instance import TestInstance
from test_automation.data_objects.test_result import TestResult
from test_automation.excpetions import DefectsExp, DefectExp
from test_automation.test_decorator.test_complete_impl import Test
from PIL.Image import Image

def main(test_Id: str):

    @Test(testId=int(testId))
    def explore(context):
        testcase: TestCase = context.get('test_case')
        test: TestInstance = context.get('test_instance')
        testresult : TestResult = TestResult()
        defects: set = set()
#         # TODO: extract the test case details printing functionality to the TestCase class
#         print(
#             f'''Started testing for case number {testcase.id} {testcase.title}
# Preconditions:
# {testcase.custom_preconds}
# Description:
# {testcase.custom_tc_description}
# Expected Results:
# {testcase.custom_expected}
# **********************
# ''')
        cli = ExploratoryTestingMenu()
        cli.start()
        while cli.is_active():
            cli.show_available_options()
            selected_option = input(">>>Please select an option?")
            outcome = ''
            try:
                outcome = cli.select(selected_option)
            except KeyError as e:
                print('Error ==========' + str(e))
            except DefectExp as new_defect:
                defects.add(new_defect)
            # inside the CLI loop each time an action is performed you need to keep adding outcome
            # (comments, screenshots, defects)
            if  isinstance(outcome, str):
                testresult.add_comment(outcome)
            elif isinstance(outcome, Path):
                testresult.attach_a_screenshot(outcome)
            # This approach is to add existing defect ids to the test result without raising them by the decorator
            elif isinstance(outcome, Defect):
                testresult.add_defect(outcome)
                # if outcome.defectId != '':
                #     testresult.add_defect(outcome)
                # else:
                #     context['test_results'] = testresult
                #     raise DefectExp(outcome)

        # This is where you add the comments and results objects to the context
        # where it will picked up by the test decorator and logged in test management
        context['test_results'] = testresult
        # this approach is to raise the new defects as exceptions and get them created by the decorator
        if testresult.defects:
            raise DefectsExp(testresult.defects)

    explore()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--testId', metavar='testId', required=True,
                        help='the testId to be executed')
    args = parser.parse_args()
    testId = args.testId
    main(test_Id=testId)