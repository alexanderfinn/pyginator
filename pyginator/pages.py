import json
import markdown
from jinja2 import FileSystemLoader, Environment, Template


class RenderingException(Exception):
    pass

class Header(object):

    def __init__(self, header):
        data = json.loads(header)
        self.fields = data.get("fields", {})
        self.template = data.get("template", None)
        self.urls = data.get("urls", None)


class Block(object):

    def __init__(self, text):
        self.name = 'body'
        self.block_type = 'html'
        lines = text.splitlines(False)
        has_header = False
        if lines[0].strip() == '':
            lines = lines[1:]
        if lines[0].strip().startswith('NAME:'):
            self.name = lines[0].split(':')[1]
            lines = lines[1:]
            has_header = True
        if lines[0].strip().startswith('TYPE:'):
            self.block_type = lines[0].split(':')[1].upper()
            lines = lines[1:]
            has_header = True

        if has_header:
            self.text = '\n'.join(lines)
        else:
            self.text = text

    def render(self, context):
        result = Template(self.text).render(**context)
        if self.block_type == 'MD':
            result = markdown.markdown(result)
        return result


class Page(object):

    BLOCK_SEPARATOR = '==='

    def __init__(self, name, text):
        blocks = self._get_blocks(text)
        self.name = name
        self.header = Header(blocks[0])
        self.blocks = [Block(b) for b in blocks[1:]]
        block_names = []
        for b in self.blocks:
            if b.name in block_names:
                raise RenderingException(
                    "More then one block with the same name '%s' for page %s" % 
                    (b.name, name))
            block_names.append(b.name)

    @classmethod
    def _get_blocks(cls, text):
        lines = text.splitlines(False)
        block = ''
        blocks = []
        for l in lines:
            if l.strip() == cls.BLOCK_SEPARATOR:
                blocks.append(block)
                block = ''
            else:
                block = '\n'.join((block, l))
        if block.strip():
            blocks.append(block)
        return blocks

    def render(self, global_context):
        rendered = {}
        context = {}
        context.update(global_context)
        context.update(self.header.fields)
        for block in blocks:
            rendered[block.name] = block.render(context)
        if not self.header.template:
            return rendered.get('body', '')
        else:
            context.update(rendered)
            template = self.jinja_env.get_template(header.template)
            return template.render(**context)

    @property
    def urls(self):
        urls = self.header.urls or (self.name,)
