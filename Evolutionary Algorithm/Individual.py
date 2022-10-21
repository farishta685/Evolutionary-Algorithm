# Written by Lelep Wighton for Evolutionary Computation 2021, Assignment 1 Group 1

# Import random
import random as rn
import math as maths


# This class represents a single solution to the Travelling Salesman Problem, randomly generated when initialised
class Individual:
    # Method for determining the fitness of an individual solution, the total round-trip distance.
    def evaluate_fitness(self):
        # Initialise total distance
        total_distance = 0

        # loop over the nodes, comparing each to the next in the sequence
        for i in range(self.num_nodes):
            # Set j to be the index of the next node in sequence
            j = i + 1
            # For the last node, the next node should be the first
            if j == self.num_nodes:
                j = 0

            # Evaluate the X and Y distances
            x_dist = self.nodes[self.solution[i]-1].x - self.nodes[self.solution[j]-1].x
            y_dist = self.nodes[self.solution[i]-1].y - self.nodes[self.solution[j]-1].y

            # Evaluate the euclidean distance
            distance = maths.sqrt(x_dist ** 2 + y_dist ** 2)

            # Add the distance to the total distance
            total_distance = total_distance + distance

        self.fitness = total_distance

    # When initialised, it should be passed the set of nodes that this TSP instance uses
    def __init__(self, nodes):
        # Store the nodes as an attribute so that the fitness evaluator can use it
        self.nodes = nodes

        # Initialise solution
        self.solution = []

        # Initialise the fitness to absurdly large number to avoid false positives
        self.fitness = 999999999999999999999999999999

        # Initialise list to hold the labels of each node
        labels = []

        # Loop over nodes, populating the list of labels
        for node in nodes:
            labels.append(node.location_num)

        # Retrieve number of nodes
        self.num_nodes = len(nodes)

        # Declare nodes_left counter
        nodes_left = self.num_nodes

        # Loop over num_nodes
        for i in range(self.num_nodes):
            # Generate random number
            index = rn.randrange(0, nodes_left)

            # Append the corresponding node's label
            self.solution.append(labels[index])

            # Remove the label that was just added
            labels.remove(labels[index])

            # Decrement nodes left counter
            nodes_left = nodes_left - 1

        # This should result in every node being visited in the solution in a random order.
        # Removal of element from list should be O(1), leaving the algorithm O(n)

        # Call evaluate_fitness
        self.evaluate_fitness()
