import unittest
import os
import sys

SRC_ROOT = os.path.join(os.path.dirname(__file__), '../src')
sys.path[0:0] = [SRC_ROOT]

import mmf

FIXTURES_ROOT = os.path.join(os.path.dirname(__file__), 'fixtures')

class MMFAPIOpenTests(unittest.TestCase):
    
    def setUp(self):
        self.mmf = mmf.api.open(os.path.join(FIXTURES_ROOT, "valid.mmf"))
    
    def test_it_should_have_config(self):
        assert hasattr(self.mmf, "config")
    
    def test_its_config(self):
        self.assertEqual(self.mmf.config, { "width": 640, "height": 400, "blocks": [] })

class MMFAPINewTests(unittest.TestCase):
    
    def setUp(self):
        self.mmf = mmf.api.new()
    
    def test_it_should_have_config(self):
        assert hasattr(self.mmf, "config")
    
    def test_its_config(self):
        self.assertEqual(self.mmf.config, {})

class MMFAPINewWithAnyPropertiesTests(unittest.TestCase):
    
    def test_it_should_have_width(self):
        self.mmf = mmf.api.new(width=640)
        self.assertEqual(self.mmf.config, { "width": 640 })
    
    def test_it_should_have_height(self):
        self.mmf = mmf.api.new(height=400)
        self.assertEqual(self.mmf.config, { "height": 400 })
    
    def test_it_should_have_blocks(self):
        self.mmf = mmf.api.new(blocks=[])
        self.assertEqual(self.mmf.config, { "blocks": [] })

if __name__ == '__main__':
    unittest.main()