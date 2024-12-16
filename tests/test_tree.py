import unittest
from geneq.tree import Node, Tree
import math

class TestEvaluateNode(unittest.TestCase):
    def setUp(self):
        self.variables = {}

    def test_addition(self):
        root = Node('+', Node(3), Node(4))
        tree = Tree(root, {}, {'+': lambda x, y: x + y})
        self.assertEqual(tree._evaluate_node(root, self.variables), 7)

    def test_subtraction(self):
        root = Node('-', Node(10), Node(4))
        tree = Tree(root, {}, {'-': lambda x, y: x - y})
        self.assertEqual(tree._evaluate_node(root, self.variables), 6)

    def test_multiplication(self):
        root = Node('*', Node(3), Node(4))
        tree = Tree(root, {}, {'*': lambda x, y: x * y})
        self.assertEqual(tree._evaluate_node(root, self.variables), 12)

    def test_division(self):
        root = Node('/', Node(8), Node(4))
        tree = Tree(root, {}, {'/': lambda x, y: x / y})
        self.assertEqual(tree._evaluate_node(root, self.variables), 2)

    def test_modulus(self):
        root = Node('%', Node(10), Node(3))
        tree = Tree(root, {}, {'%': lambda x, y: x % y})
        self.assertEqual(tree._evaluate_node(root, self.variables), 1)

    def test_exponentiation(self):
        root = Node('^', Node(2), Node(3))
        tree = Tree(root, {}, {'^': lambda x, y: x ** y})
        self.assertEqual(tree._evaluate_node(root, self.variables), 8)

    def test_sqrt(self):
        root = Node('sqrt', Node(9))
        tree = Tree(root,  {'sqrt': lambda x : x ** 0.5}, {})
        self.assertEqual(tree._evaluate_node(root, self.variables), 3)

    def test_sin(self):
        root = Node('sin', Node(math.pi / 2))
        tree = Tree(root,  {'sin': lambda x: math.sin(x)}, {})
        self.assertAlmostEqual(tree._evaluate_node(root, self.variables), 1)

if __name__ == '__main__':
    unittest.main()