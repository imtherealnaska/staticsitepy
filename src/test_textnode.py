import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase) :
    def test_eq(self) :
        node = TextNode("This is a text Node" , "bold")
        node2 = TextNode("This is a text Node" , "bold")
        self.assertEqual(node , node2)

    def test_eq_not_equal(self):
        node = TextNode("ths is text" , "normal" , None)
        node1 = TextNode("ths  s text" , "normal" , None)
        self.assertNotEqual(node , node1)

if __name__ == "__main__" :
    unittest.main()
