import os
import imp


class Processor(object):

    def __init__(self, configuration, script):
        self.configuration = configuration
        script_file_name = os.path.join(configuration.scripts_abs_path, '%s.py' % script)
        processor_script = imp.load_source("processor_script", script_file_name)
        self.script = processor_script.Processor(configuration)

    def process(self):
        pass