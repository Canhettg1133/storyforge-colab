"""Offline contract checks; no network, model download or GPU allocation."""
import ast
import base64
import hashlib
import io
import json
from html.parser import HTMLParser
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = 'StoryForge-Translator-E2B-Q4-10.ipynb'
REPO = 'HauhauCS/Gemma-4-E2B-Uncensored-HauhauCS-Aggressive'
REVISION = 'da8593c3e407afcd3e7da94ff2d69d77e2a28a48'
FILE = 'Gemma-4-E2B-Uncensored-HauhauCS-Aggressive-Q4_K_P.gguf'


class TranslatorE2B10Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = (ROOT / NAME).read_bytes()
        cls.notebook = json.loads(cls.raw)
        cls.manifest = json.loads((ROOT / 'manifest.translator-e2b10.json').read_text(encoding='utf-8'))
        code = ''.join(cls.notebook['cells'][1]['source'])
        node = next(n for n in ast.parse(code).body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == '_sf_payload' for t in n.targets))
        with zipfile.ZipFile(io.BytesIO(base64.b64decode(ast.literal_eval(node.value)))) as archive:
            cls.files = {name: archive.read(name) for name in archive.namelist()}

    def test_notebook_and_embedded_payload_match_manifest(self):
        self.assertEqual(hashlib.sha256(self.raw.replace(b'\r\n', b'\n')).hexdigest(), self.manifest['notebookSha256'])
        self.assertEqual(set(self.files), set(self.manifest['payloadSha256']))
        for name, data in self.files.items():
            self.assertEqual(hashlib.sha256(data).hexdigest(), self.manifest['payloadSha256'][name], name)
        self.assertEqual(hashlib.sha256((ROOT / 'StoryForge-Personal-AI.ipynb').read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
                         self.manifest['writerNotebookSha256'])

    def test_main_notebook_only_contains_guide_and_connection(self):
        cells = self.notebook['cells']
        self.assertEqual([c['metadata']['id'] for c in cells],
                         ['guide', 'control'])
        guide = ''.join(cells[0]['source'])
        self.assertIn('<details>', guide)
        self.assertNotIn('<details open', guide)
        self.assertIn('<summary>', guide)
        self.assertEqual(cells[1]['metadata']['cellView'], 'form')
        for cell in cells[1:]:
            self.assertFalse(cell['outputs'])
            self.assertIsNone(cell['execution_count'])
            compile(''.join(cell['source']), cell['metadata']['id'], 'exec', flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
        for name, data in self.files.items():
            if name.endswith('.py'):
                compile(data, name, 'exec')

    def test_writer_notebook_collapses_long_guide_by_default(self):
        writer = json.loads((ROOT / 'StoryForge-Personal-AI.ipynb').read_text(encoding='utf-8'))
        self.assertEqual([cell['metadata']['id'] for cell in writer['cells']], ['guide', 'control'])
        guide = ''.join(writer['cells'][0]['source'])
        self.assertIn('<details>', guide)
        self.assertNotIn('<details open', guide)
        self.assertIn('Hướng dẫn chi tiết và xử lý sự cố · bấm để xem', guide)
        self.assertEqual(writer['cells'][1]['metadata']['cellView'], 'form')

    def test_pairing_card_escapes_code_and_exposes_copy_and_feedback(self):
        code = ''.join(self.notebook['cells'][1]['source'])
        helper = next(n for n in ast.parse(code).body
                      if isinstance(n, ast.FunctionDef) and n.name == '_sf_pairing_card')
        namespace = {}
        exec(compile(ast.Module(body=[helper], type_ignores=[]), 'pairing-card', 'exec'), namespace)
        value = '\"><script>alert(1)</script>&'
        markup = namespace['_sf_pairing_card'](value)
        class Elements(HTMLParser):
            def __init__(self):
                super().__init__()
                self.elements = []
            def handle_starttag(self, tag, attrs):
                self.elements.append((tag, dict(attrs)))
        parsed = Elements()
        parsed.feed(markup)
        field = next(attrs for tag, attrs in parsed.elements if tag == 'input')
        button = next(attrs for tag, attrs in parsed.elements if tag == 'button')
        self.assertEqual(field['value'], value)
        self.assertIn('readonly', field)
        self.assertFalse(any(tag == 'script' for tag, _ in parsed.elements))
        self.assertNotIn(value, button['onclick'])
        self.assertTrue(any(attrs.get('role') == 'status' for _, attrs in parsed.elements))
        self.assertIn('Sao chép', markup)
        self.assertIn("_sf_show_pairing_code(_sf_pair['code'])", code)

    def test_default_is_pinned_e2b_q4_ten_slots_and_gpu_sampling(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'model_catalog.json').write_bytes(self.files['model_catalog.json'])
            namespace = {'__file__': str(root / 'settings.py')}
            exec(compile(self.files['settings.py'], 'settings.py', 'exec'), namespace)
            config = namespace['resolve_multiuser_settings']({}, True)
            self.assertEqual((config['repo'], config['revision'], config['filename']), (REPO, REVISION, FILE))
            self.assertEqual((config['parallel'], config['context'], config['max_tokens']), (10, 24000, 12000))
            args = namespace['model_arguments'](config, 'model.gguf', 2)
            for flag, value in (('-np', '10'), ('-c', '240000'), ('-n', '12000'), ('-ngl', '99'), ('-fa', 'on')):
                self.assertEqual(args[args.index(flag) + 1], value)
            self.assertEqual(args.count('--backend-sampling'), 1)
            self.assertNotIn('--spec-type', args)
            for changes in ({'device': 'cpu'}, {'repo': 'other/model'}, {'revision': 'main'}, {'filename': 'other.gguf'}):
                self.assertNotIn('--backend-sampling', namespace['model_arguments']({**config, **changes}, 'model.gguf', 2))
            for bad in ({'context': 12000, 'max_tokens': 12000}, {'parallel': 21}):
                with self.assertRaises(ValueError):
                    namespace['resolve_multiuser_settings'](bad, True)

    def test_pinned_engine_uses_separate_binary_root_and_keeps_lifecycle_guards(self):
        source = self.files['start_colab.py'].decode('utf-8')
        self.assertIn("RELEASE = 'b12413'", source)
        self.assertIn('/content/llama-prebuilt-b12413', source)
        self.assertIn('ensure_model_idle', source)
        self.assertIn('lease_session.is_active()', source)
        self.assertIn("publish_config(ROOT / 'translator-verified.json'", source)
        self.assertIn('start_new_session=True', source)


if __name__ == '__main__':
    unittest.main()
