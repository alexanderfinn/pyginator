import re


class ProcessingScript(object):

    def __init__(self, configuration):
        self.console = configuration.console

    def process(self, name, page):
        self.console.out('Recieved page: ' + name)
        pattern = re.compile('Some (\S*) text')
        for b in page.blocks:
            m = pattern.match(b.text)
            if m:
                self.console.out('One match found: %s' % m.group(0))
