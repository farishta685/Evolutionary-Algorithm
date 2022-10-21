# Import required libs
import copy

import numpy as np
import copy as cp


def elitism_selection(pop, number_of_selections):
    selected_individuals = []
    
    population = copy.deepcopy(pop)

    # runs through the population k times (where k is number_of_selections)
    # and in each run finds the most fit member and adds it to the selected_individuals[] 
    for i in range(number_of_selections):
        most_fit_member = population.members[0]

        for member in population.members:
            if member.fitness < most_fit_member.fitness:
                most_fit_member = member

        selected_individuals.append(most_fit_member)
        population.members.remove(most_fit_member)

    return selected_individuals



def fitness_proportional_selection(population, number_of_selections):
    selected_individuals = []
    selected_indexes = []
    fitnesses = []

    total_fitness = 0

    # the fitness of each member is inversed so that their probability of being selected
    # is the inverse of their total distance
    for i in range(len(population.members)):
        fitnesses.append(1 / population.members[i].fitness)

    for fitness in fitnesses:
        total_fitness += fitness

    selection_probabilities = [fitness / total_fitness for fitness in fitnesses]

    index_list = list(range(0, len(population.members))) 

    # Selects individuals based on probabilities in selection_probabilities[]
    for i in range(number_of_selections):
        selected_indexes.append(np.random.choice(index_list, p=selection_probabilities))

    for i in range(number_of_selections):
        selected_individuals.append(population.members[selected_indexes[i]])

    return selected_individuals




