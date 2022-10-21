# Written by Lelep Wighton for Evolutionary Computation 2021, Assignment 1 Group 1

# Import the Individual class, of which the population is made up
from Individual import Individual


# This object creates a population of individual solutions to the TSP of a given size for a given set of nodes
class Population:
    # When initialised, can accept zero or two arguments- The population size and node list respectively
    def __init__(self, *args):
        # Initialise list of population members
        self.members = []

        # If the number of arguments is two and the types match, generate the population
        if (len(args) == 2) & isinstance(args[0], int) & isinstance(args[1], list):
            pop_size = args[0]
            nodes = args[1]

            # Loop up to the size of the population
            for i in range(pop_size):
                # Initialise an individual
                current_ind = Individual(nodes)
                # Append it to the members list
                self.members.append(current_ind)

            # any number of arguments other than two will result in no additional action being taken.
