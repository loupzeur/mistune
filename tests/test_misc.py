import mistune3 as mistune
from unittest import TestCase


class TestMiscCases(TestCase):
    def test_none(self):
        self.assertEqual(mistune.html(None), '')

    def test_before_parse_hooks(self):
        def _add_name(md, state):
            state.env['name'] = 'test'

        md = mistune.create_markdown()
        md.before_parse_hooks.append(_add_name)
        state = md.block.state_cls()
        md.parse('', state)
        self.assertEqual(state.env['name'], 'test')

    def test_hard_wrap(self):
        md = mistune.create_markdown(escape=False, hard_wrap=True)
        result = md('foo\nbar')
        expected = '<p>foo<br />\nbar</p>'
        self.assertEqual(result.strip(), expected)

    def test_escape_html(self):
        md = mistune.create_markdown(escape=True)
        result = md('<div>1</div>')
        expected = '<p>&lt;div&gt;1&lt;/div&gt;</p>'
        self.assertEqual(result.strip(), expected)

        result = md('<em>1</em>')
        expected = '<p>&lt;em&gt;1&lt;/em&gt;</p>'
        self.assertEqual(result.strip(), expected)

    def test_harmful_links(self):
        result = mistune.html('[h](javAscript:alert)')
        expected = '<p><a href="#harmful-link">h</a></p>'
        self.assertEqual(result.strip(), expected)

    def test_allow_harmful_protocols(self):
        renderer = mistune.HTMLRenderer(allow_harmful_protocols=True)
        md = mistune.Markdown(renderer)
        result = md('[h](javascript:alert)')
        expected = '<p><a href="javascript:alert">h</a></p>'
        self.assertEqual(result.strip(), expected)

    def test_allow_data_protocols(self):
        renderer = mistune.HTMLRenderer(allow_harmful_protocols=['data:'])
        md = mistune.Markdown(renderer)
        result = md('[h](data:alert)')
        expected = '<p><a href="data:alert">h</a></p>'
        self.assertEqual(result.strip(), expected)

    def test_use_plugin(self):
        from mistune3.plugins.url import url
        md = mistune.Markdown(mistune.HTMLRenderer())
        md.use(url)
