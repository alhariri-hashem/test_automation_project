import jira
from jira import Issue

from test_automation.data_objects.defect import Defect
from test_automation.defect_managment.defect_managment_base import defect_managment_base_class


class jira_server(defect_managment_base_class):
    new_issue_template = {
        'project': 'TA',
        'issuetype': 'Bug',
        'priority': {'name': 'Medium'},
        'customfield_10300': {'value': 'S2-Major'},
        'labels': ['Automation'],
        'summary': '',
        'description': ''
        # 'attachment': []
        # 'customfield_10202': '1234',  # CR Number
        # 'environment': 'None'
        # 'assignee' : 'hashem.alhariri',
        # 'status' : 'Closed',
        # 'components' : [],
        # 'issuelinks' : [],
        # 'customfield_10400' : ['x'],   #release
        # 'versions' : []
    }

    def __init__(self, server: str, user_name: str, password: str):
        '''
            initializing Jira server API based on the input arguments then fetching the statuses using the api
        :param base_url: base url for the api
        :param user_name: user name
        :param password: password
        '''
        self.api = jira.client.JIRA(server=server, basic_auth=(user_name, password))

    def new_issue(self, summary: str, description: str, project_key: str = 'TA', issue_type: str = 'Bug',
                  attachment: list = None, **kwargs) -> str:
        new_bug = self.new_issue_template.copy()
        new_bug['project'] = project_key
        new_bug['issuetype'] = issue_type
        new_bug['summary'] = summary
        new_bug['description'] = description
        issue_key = self.api.create_issue(fields=new_bug).key
        for a in attachment:
            print(a)
            print(type(a))
            with open(a, 'rb') as f:
                self.api.add_attachment(issue=issue_key, attachment=f)
        print(f'new issue created {issue_key}')
        return issue_key

    def new_defect(self, defect: Defect):
        issue_key = self.new_issue(defect.summary, str(defect.description), project_key=defect.project,
                                   issue_type=defect.issue_type, attachment=defect.attachments)
        print(f'new defect created {issue_key}')
        return issue_key
