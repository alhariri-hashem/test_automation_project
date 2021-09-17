from collections import Iterable


class Defect:
    def __init__(self, defectId: str = '', summary: str = '', reproducing_steps: str = '', expected: str = '',
                 actual: str = '', logs: str = '', test_data: str = '',
                 project_key: str = 'TA', issue_type: str = 'Bug', attachments: set = (), **kwargs):
        self.defectId = defectId
        self.project = project_key
        self.issue_type = issue_type
        self.summary = summary
        # TODO: improve the formatting of defect description using templates
        self.description = {
            'Steps': reproducing_steps,
            'Expected': expected,
            'Actual': actual,
            'Test Data': test_data,
            'Logs': logs
        }
        # TODO: allow defect to be created with a list of attachments instead of single image file
        self.attachments = list()
        self.attachments.extend(attachments)

    def __str__(self):
        return self.defectId
