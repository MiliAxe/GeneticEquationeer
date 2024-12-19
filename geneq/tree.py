from typing import Optional, Union, Callable, Dict
import graphviz


class Node:
    def __init__(self, value: Union[float, str],
                 left_node: Optional['Node'] = None,
                 right_node: Optional['Node'] = None) -> None:

        self.value: Union[float, str] = value
        self.left: Optional['Node'] = left_node
        self.right: Optional['Node'] = right_node

    def __str__(self):
        if self.is_leaf():
            return str(self.value)
        elif self.right and self.left:
            return f'({self.left} {self.value} {self.right})'
        elif self.left:
            return f'{self.value}({self.left})'

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


class Tree:
    def __init__(self, root: Node, single_operators: Dict[str, Callable[[float], float]], multi_operators: Dict[str, Callable[[float, float], float]]) -> None:
        self.root = root
        self.single_operators = single_operators
        self.multi_operators = multi_operators

    def evaluate(self, variables: Dict[str, float]) -> float:
        return self._evaluate_node(self.root, variables)

    def _evaluate_node(self, node: Node, variables: Dict[str, float]) -> float:
        if not node:
            return 0
        if node and node.is_leaf():
            if node.value in variables:
                return variables[node.value]
            return node.value

        left_value = self._evaluate_node(node.left, variables)
        right_value = self._evaluate_node(node.right, variables) if node.right else 0

        if left_value in variables:
            left_value = variables[left_value]
        if right_value in variables:
            right_value = variables[right_value]

        if node.value in self.single_operators:
            return self.single_operators[node.value](left_value)
        elif node.value in self.multi_operators:
            return self.multi_operators[node.value](left_value, right_value)


    def copy(self) -> 'Tree':
        import copy

        return copy.deepcopy(self)

    def get_random_node(self, node: Node) -> Node:
        import random

        if node.is_leaf():
            return node

        random = random.random()
        if node.right is None:
            if random < 0.5:
                return node
            else:
                return self.get_random_node(node.left)
        else:
            if random < 1/3:
                return node
            elif random < 2/3:
                return self.get_random_node(node.left)
            else:
                return self.get_random_node(node.right)

    def get_random_operator(self, node: Node) -> str:
        import random

        if node.is_leaf():
            return node.value

        if node.right is None:
            return random.choice(list(self.single_operators.keys()))
        else:
            return random.choice(list(self.multi_operators.keys()))

    def __str__(self):
        return str(self.root)

            

    def visualize(self, filename: str = 'tree') -> None:
        dot = graphviz.Digraph()

        def add_nodes_edges(node: Node, parent: Optional[str] = None):
            if node is not None:
                node_id = str(id(node))
                dot.node(node_id, str(node.value))
                if parent:
                    dot.edge(parent, node_id)
                add_nodes_edges(node.left, node_id)
                add_nodes_edges(node.right, node_id)

        add_nodes_edges(self.root)
        dot.render(filename, format='png', cleanup=True)


class TreeGenerator:
    def __init__(self, variables: list[str], single_operators: dict[str, Callable[[float], float]], multi_operators: dict[str, Callable[[float, float], float]]) -> None:
        self.variables = variables
        self.single_operators = single_operators
        self.multi_operators = multi_operators

    def generate_random_tree(self, depth: int, leaf_node_chance: int = 0.3, single_operator_chance: int = 0.3, variable_chance = 0.5) -> Tree:
        return Tree(self._generate_random_tree(depth, leaf_node_chance, single_operator_chance, variable_chance), self.single_operators, self.multi_operators)
    
    def _generate_random_tree(self, depth: int, leaf_node_chance: int = 0.3, single_operator_chance: int = 0.3, variable_chance = 0.5) -> Node:
        import random

        if depth == 0 or (depth > 1 and random.random() < leaf_node_chance):
            if random.random() < variable_chance:
                return Node(random.choice(self.variables))
            else:
                return Node(random.random() * 10)

        if random.random() < single_operator_chance:
            random_operator = random.choice(list(self.single_operators.keys()))
            return Node(random_operator, self._generate_random_tree(depth - 1), None)
        else:
            random_operator = random.choice(list(self.multi_operators.keys()))
            return Node(random_operator, self._generate_random_tree(depth - 1), self._generate_random_tree(depth - 1))


if __name__ == '__main__':
    single_operators = {
        'sqrt': lambda x: x ** 0.5
    }

    multi_operators = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
        '%': lambda x, y: x % y,
        '^': lambda x, y: x ** y
    }

    # Example tree construction
    random_tree_node= TreeGenerator(['x', 'y'], single_operators, multi_operators).generate_random_tree(10, 0.1, 0.3, 0.5)
    tree = Tree(random_tree_node, single_operators, multi_operators)


    # Visualize the tree
    tree.visualize('example_tree')

    print(tree.root)
