import os
import json
import shutil
from jinja2 import FileSystemLoader, Environment, Template


class Header(object):

    def __init__(self, header):
        data = json.loads(header)
        self.fields = data.get("fields", {})
        self.template = data.get("template", None)
        self.urls = data.get("urls", None)


class Builder(object):

    HEADER_SEPARATOR = '===\n'

    def __init__(self, configuration):
        self.configuration = configuration
        self.jinja_env = Environment(loader=FileSystemLoader(self.configuration.templates_abs_path))

    def build(self):
        try:
            shutil.rmtree(self.configuration.target_path)
        except:
            pass
        for f in os.listdir(self.configuration.sources_abs_path):
            if f.endswith('.html'):
                text, header = self.render(f)
                if not header.urls:
                    header.urls = (f,)
                for url in header.urls:                    
                    target = self.get_target_file(url)
                    target.write(text)
                    target.close()
        self.copy_static()

    def copy_static(self):
        for folder in self.configuration.static_folders:
            shutil.copytree(os.path.join(self.configuration.base_path, folder), os.path.join(self.configuration.target_path, folder))


    def render(self, file):
        header, html = self.read_file(file)
        context = header.fields
        context.update(self.configuration.fields)
        body = Template(html).render(**context)
        if not header.template:
            return body, header
        else:
            context.update({'body': body})
            template = self.jinja_env.get_template(header.template)
            return template.render(**context), header

    def read_file(self, file):
        f = open(os.path.join(self.configuration.sources_abs_path, file), 'r')
        header = ''
        html = ''
        is_header = True
        for line in f:
            if is_header:
                if line == self.HEADER_SEPARATOR:
                    is_header = False
                else:
                    header = header + line
            else:
                html = html + line
        return Header(header), html

    def get_target_file(self, url):
        if self.configuration.pretty_urls and not url.endswith('.html'):
            target = os.path.join(self.configuration.target_path, url, 'index.html')
        else:
            target = os.path.join(self.configuration.target_path, url)
        try:
            os.makedirs(os.path.dirname(target))
        except:
            pass
        return open(target, 'w')


