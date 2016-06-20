import os
import imp
from builder import Builder


class Processor(object):

    def __init__(self, configuration, script):
        self.configuration = configuration
        script_file_name = os.path.join(configuration.scripts_abs_path, '%s.py' % script)
        script_mod = imp.load_source("script_mod", script_file_name)
        if hasattr(script_mod, 'ProcessingScript'):
            self.script = script_mod.ProcessingScript(configuration)
        else:
            self.script = None

    def process(self):
        modified = 0
        if not self.script:
            return modified
        builder = Builder(self.configuration)
        for source in builder.source_files:
            page = builder.get_page(source)
            mod_page = self.script.process(source, page)
            if mod_page:
                f = open(source, 'w')
                f.write(page.get_text())
                f.close()
                modified += 1
        return modified
