import unittest
from pyginator.pages import Block


class BlockTest(unittest.TestCase):

    def test_simple_block(self):
        text = 'This is the most simplistic block'
        block = Block(text)
        self.assertEqual(block.name, 'body')
        self.assertEqual(block.block_type, 'html')
        self.assertEqual(block.text, text)

    def test_with_name(self):
        name_text = 'NAME:test'
        block_text = 'This is the most simplistic block'
        text = '\n'.join((name_text, block_text))
        block = Block(text)
        self.assertEqual(block.name, 'test')
        self.assertEqual(block.block_type, 'html')
        self.assertEqual(block.text, block_text)

    def test_with_name_and_type(self):
        name_text = 'NAME:test'
        type_text = 'TYPE:md'
        block_text = 'This is the most simplistic block'
        text = '\n'.join((name_text, type_text, block_text))
        block = Block(text)
        self.assertEqual(block.name, 'test')
        self.assertEqual(block.block_type, 'MD')
        self.assertEqual(block.text, block_text)

    def test_multiline(self):
        name_text = 'NAME:abc d e f'
        type_text = 'TYPE:md'
        block_text = 'This is the\nmultiline\nblock'
        text = '\n'.join((name_text, type_text, block_text))
        block = Block(text)
        self.assertEqual(block.name, 'abc d e f')
        self.assertEqual(block.block_type, 'MD')
        self.assertEqual(block.text, block_text)

    def test_with_spaces(self):
        name_text = '  NAME:abc d e f'
        type_text = '  TYPE:md'
        block_text = '  This is the\nmultiline\nblock'
        text = '\n'.join((name_text, type_text, block_text))
        block = Block(text)
        self.assertEqual(block.name, 'abc d e f')
        self.assertEqual(block.block_type, 'MD')
        self.assertEqual(block.text, block_text)
