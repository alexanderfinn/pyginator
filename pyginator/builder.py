import os
import shutil
from pages import Page


class Builder(object):

    def __init__(self, configuration):
        self.configuration = configuration
        self.jinja_env = Environment(loader=FileSystemLoader(self.configuration.templates_abs_path))
        self.extra_data = {}
        self.global_context = self.configuration.fields

    def build(self):
        try:
            shutil.rmtree(self.configuration.target_path)
        except:
            pass
        for f in os.listdir(self.configuration.sources_abs_path):
            if f.endswith('.html'):
                try:
                    page = self.render(f)
                    for url in page.urls:
                        target = self.get_target_file(url)
                        target.write(text.encode('utf-8'))
                        target.close()
                except RenderingException, e:
                    print "Failed to render page %s with exception: %s" % (f, e)
        self.copy_static()

    def copy_static(self):
        for folder in self.configuration.static_folders:
            shutil.copytree(os.path.join(self.configuration.base_path, folder), os.path.join(self.configuration.target_path, folder))


    def render(self, file):
        print "Reading file " + file
        f = open(os.path.join(self.configuration.sources_abs_path, file), 'r')
        return Page(file, f.read())

    def get_target_file(self, url):
        target = os.path.join(self.configuration.target_path, url)
        if self.configuration.pretty_urls and not url.endswith('.html'):
            target = os.path.join(target, 'index.html')
        try:
            os.makedirs(os.path.dirname(target))
        except:
            pass
        return open(target, 'w')
