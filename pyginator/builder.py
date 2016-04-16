import os
import json
import shutil
import markdown
from jinja2 import FileSystemLoader, Environment, Template


class Header(object):

    def __init__(self, header):
        data = json.loads(header)
        self.fields = data.get("fields", {})
        self.template = data.get("template", None)
        self.urls = data.get("urls", None)
        self.data_files = data.get("data", [])


class Builder(object):

    HEADER_SEPARATOR = '===\n'

    def __init__(self, configuration):
        self.configuration = configuration
        self.jinja_env = Environment(loader=FileSystemLoader(self.configuration.templates_abs_path))
        self.extra_data = {}

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
                    target.write(text.encode('utf-8'))
                    target.close()
        self.copy_static()

    def copy_static(self):
        for folder in self.configuration.static_folders:
            shutil.copytree(os.path.join(self.configuration.base_path, folder), os.path.join(self.configuration.target_path, folder))


    def render(self, file):
        header, html = self.read_file(file)
        context = header.fields
        context.update(self.get_data(header))
        context.update(self.configuration.fields)
        body = Template(html.decode('utf-8')).render(**context)
        if file.endswith('.md'):
            body = markdown.markdown(body)
        if not header.template:
            return body, header
        else:
            context.update({'body': body})
            template = self.jinja_env.get_template(header.template)
            return template.render(**context), header

    def get_data(self, header):
        result = {}
        for df in header.data_files:
            if not df in self.extra_data:
                self.load_extra_data(df)
            result[df] = self.extra_data.get(df, {})
        return result

    def load_extra_data(self, df):
        f = open(os.path.join(self.configuration.data_path, df), 'r')
        try:
            self.extra_data[df] = json.loads(f.read())
        except:
            print "Failed to load extra data %s" % df
        f.close()

    def read_file(self, file):
        print "Reading file " + file
        f = open(os.path.join(self.configuration.sources_abs_path, file), 'r')
        is_header = True
        fc = f.read()
        header, html = fc.split('===')
        return Header(header), html

    def get_target_file(self, url):
        target = os.path.join(self.configuration.target_path, url)
        if self.configuration.pretty_urls and not url.endswith('.html'):
            target = os.path.join(target, 'index.html')
        try:
            os.makedirs(os.path.dirname(target))
        except:
            pass
        return open(target, 'w')
