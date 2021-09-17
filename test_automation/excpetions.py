from test_automation.data_objects.defect import Defect


class CustomException(Exception):
    pass


class DefectManagementException(CustomException):
    pass


class TestManagementException(CustomException):
    pass


class ParametersNotProvided(TestManagementException):
    def __init__(self, error):
        self.error = error


#
class DefectExp(CustomException):
    def __init__(self, defect: Defect):
        self.defect = defect


class DefectsExp(DefectExp):
    def __init__(self, defects: set):
        self.defect_set = list()
        self.defect_set.extend(defects)
