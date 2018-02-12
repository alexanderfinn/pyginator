import os
import shutil
from pages import Page, RenderingException


class Builder(object):

    def __init__(self, configuration):
        self.configuration = configuration
        self.extra_data = {}
        self.global_context = self.configuration.fields

    def build(self):
        try:
            shutil.rmtree(self.configuration.target_path)
        except:
            pass
        for source in self.source_files:
            try:
                self.configuration.console.out("Building file %s" % source)
                page = self.get_page(source)
                for url in page.urls:
                    target = self.get_target_file(url)
                    target.write(page.render(self.global_context).encode('utf-8'))
                    target.close()
            except RenderingException, e:
                print "Failed to render page %s with exception: %s" % (f, e)
        self.copy_static()

    def get_page(self, source):
        f = open(source, 'r')
        page = Page(os.path.split(source)[1], f.read(), templates_dir=self.configuration.templates_abs_path)
        f.close()
        return page


    @property
    def source_files(self):
        for f in os.listdir(self.configuration.sources_abs_path):
            if f.endswith('.html') or f.endswith('.txt'):
                yield os.path.join(self.configuration.sources_abs_path, f)

    def copy_static(self):
        for folder in self.configuration.static_folders:
            shutil.copytree(os.path.join(self.configuration.base_path, folder), os.path.join(self.configuration.target_path, folder))

    def get_target_file(self, url):
        target = os.path.join(self.configuration.target_path, url)
        if self.configuration.pretty_urls and not url.endswith('.html'):
            target = os.path.join(target, 'index.html')
        try:
            os.makedirs(os.path.dirname(target))
        except:
            pass
        return open(target, 'w')
