import unittest
from pyginator.configuration import Configuration
from pyginator.output import Console


class TestConsole(Console):

    def __init__(self):
        self.messages = []

    def out(self, message):
        self.messages.append(message)

class FunctionalTestCase(unittest.TestCase):

    test_dir = './test_project'

    @property
    def configuration(self):
        if not hasattr(self, '_configuration'):
            self._configuration = Configuration(self.test_dir, {})
            self._configuration.console = TestConsole()
        return self._configuration