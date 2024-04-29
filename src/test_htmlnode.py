import unittest

from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase) :
    def test_eq(self) :
        node = HTMLNode("h1")
        print(node)

if __name__ == "__main__" :
    unittest.main()
