# -*- coding: utf-8 -*-
import yaml_reader
import unittest




class TestEnhancedYaml(unittest.TestCase):

    def test_with_file(self):
        config = yaml_reader.YamlReader('./application.yaml').config
        self.assertEqual(config['root']['b1']['k1'], 'v1')
        self.assertEqual(config['root']['b2']['k1'], config['root']['b1']['k1'])

    def test_with_string(self):
        src = '''root:
  b1:
    k1: v1
  b2:
    k1: ${root.b1.k1}
'''
        config = yaml_reader.YamlReader(config=src).config
        self.assertEqual(config['root']['b1']['k1'], 'v1')
        self.assertEqual(config['root']['b2']['k1'], config['root']['b1']['k1'])

if __name__ == '__main__':
    unittest.main()

