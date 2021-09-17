import pathlib

import requests
from jira import JIRAError
from requests.exceptions import MissingSchema, RequestException
from testrail_api import StatusCodeError

from test_automation.excpetions import TestManagementException, DefectManagementException, CustomException
from test_automation.test_decorator.test_decorator_base import TestBase
from test_automation.test_managment.test_rail_impl import test_rail
from test_automation.defect_managment.jira_server_impl import jira_server
import configparser


def create_default_config():
    config = configparser.ConfigParser()
    config.add_section("TestRail")
    config['TestRail']['url'] = "testrail_url"
    config['TestRail']['user_name'] = "testrail_user_name"
    config['TestRail']['password'] = "testrail_password"
    config.add_section("Jira")
    config['Jira']['url'] = "jira_url"
    config['Jira']['user_name'] = "jira_user_name"
    config['Jira']['password'] = "jira_password"
    config_path = pathlib.Path.home() / 'test_automation'
    if not config_path.exists():
        config_path.mkdir()
    with open(pathlib.Path.home() / 'test_automation/conf.ini', 'w') as config_file:
        config.write(config_file)
    return config_path / 'conf.ini'


class Test(TestBase):
    def __init__(self, runId: int = -1, caseId: int = -1, testId: int = -1, context: dict = {}):
        config = configparser.ConfigParser()
        config_file = pathlib.Path.home() / 'test_automation/conf.ini'
        if config.read(config_file):
            testrail_url = config['TestRail']['url']
            testrail_user_name = config['TestRail']['user_name']
            testrail_password = config['TestRail']['password']
            jira_url = config['Jira']['url']
            jira_user_name = config['Jira']['user_name']
            jira_password = config['Jira']['password']
        else:
            config_file = create_default_config()
            raise CustomException(f"Invalid Configuration. please check configuration file {config_file}")
        try:
            _testrail = test_rail(testrail_url, testrail_user_name, testrail_password)
            _jira = jira_server(jira_url, jira_user_name, jira_password)

            super().__init__(test_management=_testrail, defect_management=_jira, runId=runId,
                             caseId=caseId, testId=testId, context=context)
        # TODO: Improve exception handling
        except MissingSchema as e:
            raise DefectManagementException(f"check configuration file at {config_file} ")
        except JIRAError as e:
            raise DefectManagementException(f"check configuration file at {config_file} ")
        except StatusCodeError as e:
            TestManagementException(f"check configuration file at {config_file} ")
        except Exception as e:
            print(type(e))

