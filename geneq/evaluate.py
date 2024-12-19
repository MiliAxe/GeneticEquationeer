import numpy as np
import math
import matplotlib.pyplot as plt
from tree import TreeGenerator, Tree
from evolution import SymbolicRegressor


# Define a function to generate sample data points
def generate_data(func, x_range, num_points):
    X = np.linspace(x_range[0], x_range[1], num_points)
    y = func(X)
    return X, y

# Define a sample function to approximate
# def sample_function(x):
#     return np.sin(x) + 0.1 * np.random.randn(len(x)) * np.cos(x) * x

def sample_function(x):
    return np.sin(x) + 0.1 * np.random.randn(len(x)) * np.cos(x) * x

X, y = generate_data(sample_function, x_range=(-10, 10), num_points=500)

# Initialize the TreeGenerator and SymbolicRegressor
tree_generator = TreeGenerator(['x'], {'sin': math.sin, 'cos': math.cos}, {'+': lambda x, y: x + y, '*': lambda x, y: x * y, '-': lambda x, y: x - y})
symbolic_regressor = SymbolicRegressor(tree_generator=tree_generator, initial_population_size=100, generations=20, initial_population_depth=5)

# Fit the model to the data
symbolic_regressor.fit(X, y)

# Predict the values using the fitted model
y_pred = symbolic_regressor.predict(X)

print(symbolic_regressor.get_prediction_equation())


# Plot the original data points and the predicted values
plt.scatter(X, y, color='blue', label='Original Data')
plt.plot(X, y_pred, color='red', label='Fitted Curve')
plt.legend()
plt.xlabel('X')
plt.ylabel('y')
plt.title('Symbolic Regression with Genetic Programming')
plt.savefig('symbolic_regression.png')