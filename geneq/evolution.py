from tree import TreeGenerator, Tree
import numpy as np
import pandas as pd


class SymbolicRegressor:
    def __init__(self, tree_generator: TreeGenerator, initial_population_size: int = 100, generations: int = 20, initial_population_depth: int = 100) -> None:
        self.tree_generator = tree_generator
        self.initial_population_size = initial_population_size
        self.generations = generations
        self.initial_population_depth = initial_population_depth
        self.population = pd.DataFrame(columns=['tree', 'fitness'])

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        self.population['tree'] = [self.tree_generator.generate_random_tree(
            self.initial_population_depth) for _ in range(self.initial_population_size)]

        self.population['fitness'] = self.population['tree'].apply(
            lambda tree: self._calculate_fitness(tree, X, y))

        for _ in range(self.generations):
            self._evolve(X, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        best_tree = self.population.loc[self.population['fitness'].idxmin(
        )]['tree']
        result = np.array([best_tree.evaluate({'x': x}) for x in X])
        return result

    def get_prediction_equation(self) -> str:
        best_tree = self.population.loc[self.population['fitness'].idxmin(
        )]['tree']
        return str(best_tree)

    def _calculate_fitness(self, tree: Tree, X: np.ndarray, y: np.ndarray) -> float:
        prediction = np.array([tree.evaluate({'x': x}) for x in X])
        return np.sum((prediction - y) ** 2)

    def _crossover(self, tree1: Tree, tree2: Tree) -> tuple[Tree, Tree]:
        tree1_copy = tree1.copy()
        tree2_copy = tree2.copy()
        if tree1_copy.root.is_leaf() or tree2_copy.root.is_leaf():
            return tree1_copy, tree2_copy
        node1 = tree1.get_random_node(tree1.root)
        while node1.is_leaf():
            node1 = tree1.get_random_node(tree1.root)
        node2 = tree2.get_random_node(tree2.root)
        while node2.is_leaf():
            node2 = tree2.get_random_node(tree2.root)

        import random
        random = random.random()
        if random < 0.5:
            node1.left, node2.left = node2.left, node1.left
        else:
            node1.right, node2.right = node2.right, node1.right

        return tree1_copy, tree2_copy

    def _mutate(self, tree: Tree) -> Tree:
        tree_copy = tree.copy()
        node = tree_copy.get_random_node(tree_copy.root)
        node.value = tree_copy.get_random_operator(node)
        return tree

    def _select_parents(self, parent_count: int, tournament_size: int = 5) -> pd.DataFrame:
        parents_list = []
        population_copy = self.population.copy()
        for _ in range(parent_count):
            selected_parent = self._tournament_selection(population_copy, tournament_size)
            parents_list.append(selected_parent)
            population_copy = population_copy.drop(selected_parent.name)
        parents = pd.concat(parents_list, axis=1).T.reset_index(drop=True)
        return parents

    def _tournament_selection(self, population: pd.DataFrame, tournament_size: int = 5) -> pd.Series:
        actual_tournament_size = min(tournament_size, len(population))
        tournament = population.sample(actual_tournament_size)
        winner = tournament.loc[tournament['fitness'].idxmin()]
        return winner

    def _evolve(self, X: np.ndarray, y: np.ndarray, mutation_rate: float = 0.1, crossover_rate: float = 0.1) -> None:
        """
        One generation of evolution
        The steps are:
        1. Evaluate the fitness of each individual in the population
        2. Select parents for the next generation (Individuals with higher fitness are more likely to be selected)
        3. Apply crossover and mutation to create the next generation
        4. Repeat until the number of generations is reached
        5. Return the best individual
        """
        parents = self._select_parents(parent_count=self.initial_population_size)

        parents['fitness'] = parents['tree'].apply(
            lambda tree: self._calculate_fitness(tree, X, y))

        new_trees = []
        for parent in parents['tree']:
            if np.random.rand() < crossover_rate:
                selected_tree = self._tournament_selection(parents)["tree"]
                new_tree1, new_tree2 = self._crossover(parent, selected_tree)
                new_trees.append({'tree': new_tree1, 'fitness': self._calculate_fitness(new_tree1, X, y)})
                new_trees.append({'tree': new_tree2, 'fitness': self._calculate_fitness(new_tree2, X, y)})

        if new_trees:
            parents = pd.concat([parents, pd.DataFrame(new_trees)], ignore_index=True)

        # mutated_trees = []
        # for parent in parents['tree']:
        #     if np.random.rand() < mutation_rate:
        #         mutated_parent = self._mutate(parent)
        #         mutated_trees.append({'tree': mutated_parent, 'fitness': self._calculate_fitness(mutated_parent, X, y)})

        # if mutated_trees:
        #     parents = pd.concat([parents, pd.DataFrame(mutated_trees)], ignore_index=True)

        self.population = parents
