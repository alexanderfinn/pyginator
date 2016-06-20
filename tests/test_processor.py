from testlib import FunctionalTestCase
from pyginator.processor import Processor
from pyginator.configuration import Configuration


class ProcessorTest(FunctionalTestCase):

    def test_process_basics(self):
        processor = Processor(self.configuration, 'test_script')
        modified = processor.process()
        self.assertEqual(len(self.configuration.console.messages), 2)
        self.assertEqual(self.configuration.console.messages[1], 'One match found: Some block text')