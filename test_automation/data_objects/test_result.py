from collections import OrderedDict
from pathlib import Path

from PIL.Image import Image

from test_automation.data_objects.defect import Defect


class TestResult:
    def __init__(self):
        self.comments = set()
        self.attachments = list()
        self.defects = set()

    def add_comment(self, comment: str):
        if comment is not None and comment != '':
            self.comments.add(comment)

    def get_comments(self):
        return '\n'.join(self.comments)

    def attach_a_screenshot(self, outcome: Path):
        self.attachments.append(outcome)

    def get_attachments(self):
        return self.attachments

    def add_defect(self, d: Defect):
        if d is not None:
            self.defects.add(d)

    def get_defects(self):
        return self.defects

