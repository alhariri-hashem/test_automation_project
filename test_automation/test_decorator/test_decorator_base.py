from datetime import datetime

from test_automation.data_objects.defect import Defect
from test_automation.defect_managment import defect_managment_base
from test_automation.excpetions import ParametersNotProvided, DefectExp, CustomException, DefectsExp
# from test_complete_decorator import do_nothing_and_return
from test_automation.test_managment import test_managment_base


def do_nothing_and_return(*args, **kwargs):
    '''
    Just an empty runnable function that does nothing to replace the test when preconditions are not met
    :param args:  will be ignored
    :param kwargs: will be ignored
    :return: No return
    '''
    pass


class TestBase(object):

    def __init__(self, test_management: test_managment_base, defect_management: defect_managment_base, runId: int = -1,
                 caseId: int = -1, testId: int = -1, context: dict = {}):
        if (caseId > 0 or runId > 0) and (testId > 0):
            raise ParametersNotProvided('CaseID+RunID or TestID must be provided')
        self.test_management = test_management
        self.defect_management = defect_management
        self.start_time = None
        self.finish_time = None
        self.caseId = caseId
        self.testId = testId
        self.runId = runId
        self.status = 'untested'
        self.test_results = None
        self.comments = ''
        self.attachments = None
        self.defects = set()
        self.pre_conditions_met = False
        # TODO: define other elements of a test case like title, description, points to be tested, expected results, steps ...
        self.return_function = do_nothing_and_return
        self.context = context

    def __call__(self, f, *args, **kwargs):
        def inner_func(*args, **kwargs):
            self.add_artifacts_to_context()
            self.check_pre_conditions()
            if self.pre_conditions_met:
                try:
                    self.start()
                    self.return_function = f(*args, context=self.context, **kwargs)
                    self.passed()
                except DefectsExp as e:
                    self.failed(e.defect_set)
                    print(e.defect_set)
                    self.return_function = do_nothing_and_return
                except DefectExp as e:
                    defect_set = set()
                    defect_set.add(e)
                    self.failed(defect_set)
                    self.return_function = do_nothing_and_return
                except CustomException as e:
                    print(e)
            else:
                self.blocked()
                self.return_function = do_nothing_and_return
            return self.return_function

        return inner_func

    def add_artifacts_to_context(self):
        if self.caseId > 0:
            self.context['test_case'] = self.test_management.get_test_case(self.caseId)
        elif self.testId > 0:
            self.context['test_instance'] = self.test_management.get_test_instance(self.testId)
            self.caseId = self.context['test_instance'].case_id
            self.context['test_case'] = self.test_management.get_test_case(self.caseId)

    def check_pre_conditions(self):
        # TODO: verify the preconditions and update the flag to control the status of the test.
        self.pre_conditions_met = True  # for now pre conditions are always met. still thinking how to implement this
        # self.defects.add('preconditions')

    def start(self):
        self.start_time = datetime.now()
        # print(F'Started execution for test {self.caseId} under run {self.runId} at {self.start_time}')

    def finish(self):
        self.finish_time = datetime.now()
        self.test_results = self.context.get('test_results')
        if self.test_results is not None:
            self.comments = self.test_results.get_comments()
            # print(self.comments)
            self.attachments = self.test_results.get_attachments()
            # print(self.attachments)
            self.defects = self.test_results.get_defects()
            # print(self.defects)
            # print(F'Finished execution for test {self.testId} under run {self.runId} at {self.finish_time}')

    def get_elapsed_in_ms(self) -> str:
        elapsed_in_ms = int((self.finish_time - self.start_time).total_seconds())
        if elapsed_in_ms <= 0:
            elapsed_in_ms = 1
        return str(elapsed_in_ms) + 's'

    def passed(self):
        self.finish()
        self.status = 'passed'
        self.test_management.add_result(status=self.status, run_id=self.runId, case_id=self.caseId, test_id=self.testId,
                                        elapsed=self.get_elapsed_in_ms(), comments=self.comments,
                                        attachments=self.attachments, defects=self.defects)

    def failed(self, failures: set):
        self.finish()
        self.status = 'failed'
        print(failures)
        # TODO: check configuration if log defect is enabled then raise the issue in Jira then linke it with the test case
        for f in failures:
            if isinstance(f, DefectExp):
                if f.defect.defectId == '':
                    new_issue = self.defect_management.new_defect(f.defect)
                    f.defect.defectId = new_issue
                    self.defects.add(f.defect)
                self.defects.add(f.defect)
            elif isinstance(f, Defect):
                if f.defectId == '':
                    new_issue = self.defect_management.new_defect(f)
                    f.defectId = new_issue
                self.defects.add(f)
            else:
                new_issue = self.defect_management.new_issue(summary=str(f.__class__), description=str(f.__cause__))
                self.defects.add(Defect(new_issue))

        self.test_management.add_result(status=self.status, run_id=self.runId, case_id=self.caseId, test_id=self.testId,
                                        defects=self.defects, elapsed=self.get_elapsed_in_ms(),
                                        comments=self.comments, attachments=self.attachments)

    def blocked(self):
        self.finish()
        self.status = 'blocked'
        elapsed_in_ms = str(int((self.finish_time - self.start_time).total_seconds())) + 's'
        # TODO: get the list of issues from the pre condition case and link it with the this test case
        self.test_management.add_result(status=self.status, run_id=self.runId, case_id=self.caseId, test_id=self.testId,
                                        defects=self.defects, elapsed=self.get_elapsed_in_ms(), comments=self.comments,
                                        attachments=self.attachments)
