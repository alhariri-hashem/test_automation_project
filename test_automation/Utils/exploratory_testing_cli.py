import argparse
import datetime
import pathlib
from collections import ChainMap
from pathlib import Path

import PIL.Image

from test_automation.Utils.menu import Menu
from test_automation.Utils.menu_item import MenuItem
from test_automation.data_objects.defect import Defect
from test_automation.excpetions import DefectExp


def capture_screenshot():
    import PIL.ImageGrab
    im = PIL.ImageGrab.grab()
    im = im.resize((800, 500))
    # TODO: Find the best resolution to use
    screenshots_path = pathlib.Path.home() / 'test_automation/screenshots'
    if not screenshots_path.exists():
        screenshots_path.mkdir()
    path = screenshots_path / pathlib.Path(f'{datetime.datetime.now().strftime("%Y%b%d%H%M%S%f")}.jpeg')
    im.save(path)
    return path.absolute()


class ExploratoryTestingMenu:
    def __init__(self):
        self.home_option = Menu()
        self.home_option.add(self.home)
        # self.home_option.add(self.back)
        self.home_option.add(self.exit)

        self.options = Menu()
        self.options.add(self.add_a_comment)
        self.options.add(self.attache_a_screenshot)
        self.options.add(self.link_a_defect)
        self.options.add(self.create_a_defect)

        self.add_another_comment_menu = Menu()
        self.add_another_comment_menu.add(self.add_another_comment)

        self._isActive = False
        self._available_options = ChainMap(self.home_option.get_dict())

    def start(self):
        self._isActive = True
        self._available_options = self._available_options.new_child(self.options.get_dict())

    def is_active(self):
        return self._isActive

    def show_available_options(self):
        for o in self._available_options.keys():
            self._available_options[o].show()

    def select(self, option):
        selected = self._available_options.get(option)
        if selected:
            return selected.action(self)
        else:
            raise KeyError(f"Selected option {option} not found")

    @MenuItem('h', 'Home')
    def home(self):
        self._available_options.maps.clear()
        self._available_options = self._available_options.new_child(self.home_option.get_dict())
        self._available_options = self._available_options.new_child(self.options.get_dict())

    @MenuItem('b', 'Back')
    def back(self):
        self._available_options = self._available_options.parents

    @MenuItem('x', 'Exit')
    def exit(self):
        self._isActive = False
        if input("Done! would you like to save?") in ['Y', 'y', 'yes', 'Yes']:
            print('Saved')
        else:
            print('Discarded')

    @MenuItem('1', 'Add a Comment')
    def add_a_comment(self):
        comment = input("Please enter your comment:")
        print("Noted! your comment is saved")
        self._available_options = self._available_options.new_child(self.add_another_comment_menu.get_dict())
        return comment

    @MenuItem('1', 'Add another comment')
    def add_another_comment(self):
        comment = input("Add another comment?")
        print("Noted! your comment is saved")
        return comment

    @MenuItem('2', 'Attache a screenshot')
    def attache_a_screenshot(self):
        print("OK, Attaching a screenshot")
        return capture_screenshot()

    @MenuItem('3', 'Link to an existing defect')
    def link_a_defect(self):
        print("Linking to an existing defect")
        response = input('Please inter the defect ID?')
        d = Defect(defectId=response)
        return d

    @MenuItem('4', 'Create a new defect')
    def create_a_defect(self):
        print("Creating a defect")
        # project = input('project: TA')
        summery = input('Summery: ')
        # issue_type = input('Issue Type: Bug?')
        reproducing_steps = input('reproducing_steps: ')
        expected = input('Expected: ')
        actual = input('Actual: ')
        test_data = input('Test Data: ')
        logs = input('Logs: ')
        description = {
            'Steps': reproducing_steps,
            'Expected': expected,
            'Actual': actual,
            'Test Data': test_data,
            'Logs': logs
        }
        attachments = set()
        attachments.add(capture_screenshot())

        d = Defect(summary=summery, reproducing_steps=reproducing_steps, expected=expected, actual=actual,
                   test_data=test_data, logs=logs, attachments=attachments)
        # with PIL.Image.open('1.jpeg', 'r') as im:
        #     d.attachments.append(im)
        return d
