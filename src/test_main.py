import unittest
from main import extract_title

class TestMain(unittest.TestCase):

    def test_return(self):
        md_text = "# This is a title for a test"
        not_md_test = "## This title should fail"

        self.assertEqual(extract_title(md_text), 'This is a title for a test')
        #self.assertNotEqual(extract_title(not_md_test), 'This is a title for a test')