import unittest
from pyginator.pages import Page, RenderingException


class PageTest(unittest.TestCase):


    def test_get_blocks_basic(self):
        text = "aaa\nbbb\n===\nccc\nddd\n===\nxxx\nyyy"
        blocks = Page._get_blocks(text)
        self.assertEqual(len(blocks), 3)

    def test_get_blocks_complex(self):
        text = "aaa\nbbb\n  ===   \nccc\nddd\n===    \nxxx\nyyy"
        blocks = Page._get_blocks(text)
        self.assertEqual(len(blocks), 3)

    def test_new_page(self):
        text = '''{"urls": ["index.html"]}
        ===
        Text Block
        '''

        page = Page('test', text)
        self.assertEqual(len(page.blocks), 1)

    def test_new_page_multiple_blocks(self):
        text = '''{"urls": ["index.html"]}
        ===
        Text Block
        ===
        NAME:aaa
        Another block
        ===
        NAME:bbbb

        Yet another block
        '''
        page = Page('test', text)
        self.assertEqual(len(page.blocks), 3)

    def test_new_page_header_only(self):
        text = '''{"urls": ["index.html"]}
        ===
        '''
        page = Page('test', text)
        self.assertEqual(len(page.blocks), 0)

    def test_new_page_header_only_without_separator(self):
        text = '''{"urls": ["index.html"]}'''
        page = Page('test', text)
        self.assertEqual(len(page.blocks), 0)

    def test_page_no_same_block_names(self):
        text = '''{"urls": ["index.html"]}
        ===
        Text Block
        ===
        NAME:a
        Another block
        ===

        Yet another block
        '''
        try:
            page = Page('test', text)
            self.fail('Should fail for page with multiple blocks having same name')
        except RenderingException, e:
            pass

    def test_get_text(self):
        text = '''{"urls": ["index.html"]}
        ===
        Text Block
        ===
        NAME:a
        Another block
        '''
        expected_text = '{"urls": ["index.html"]}\n===\nNAME:body\nTYPE:HTML\n\n        Text Block\n===\nNAME:a\nTYPE:HTML\n        Another block\n        '
        page = Page('test', text)
        self.assertEqual(page.get_text(), expected_text)