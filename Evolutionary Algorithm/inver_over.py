import pandas as pd
import copy
import sys
import statistics
import numpy as np
import random as rn
import math as maths
from Population import *
from ParseNodeFile import *
import time

start_time = time.time()


# Inversion Mutation
def inversion(inputList, b, e):
    s = inputList

    stop = 0
    start = 0

    # checking for minimum value to swap
    if min(b, e) == b:
        start = b
        stop = e
    else:
        start = e
        stop = b

    size = stop + start
    for i in range(start, (size + 1) // 2):
        j = size - i
        s[i], s[j] = s[j], s[i]

    return s


def inver_over(prob, filename):
    # random initialisation of the population p
    node_array = parse_node_file(filename)
    pop = Population(50, node_array)

    pop_fitness = []
    for ind in pop.members:
        pop_fitness.append(ind.fitness)
    start_fitness = sum(pop_fitness)

    # while (not satisfied termination condition)
    generation = 0
    while generation < 20000:
        print("Running generation {gn}".format(gn = generation))
        # for each individual
        for s in pop.members:
            s_prime = copy.deepcopy(s)

            # population.members[i].solution  = individual.solution = individual_prime.solution holds the list of cities. We are making a random choice from the available cities.

            # select (randomly) a city from s_prime
            c = rn.choice(s_prime.solution)
            while True:
                # if rand <= probability of choosing, then select c_prime from the remaining cities.
                if rn.random() <= prob:

                    # if prob -> 1, then c_prime is likely a random city in s_prime (original individual)
                    # if prob -> 0, then c_prime is likely the city c+1 in a random individual s_secondary

                    # select c_prime, need to remove selecting same city?
                    c_prime = rn.choice(s_prime.solution)

                    while c_prime == c:
                        c_prime = rn.choice(s_prime.solution)


                else:
                    # choose another random individual
                    s_secondary = rn.choice(pop.members)
                    while s_secondary == s_prime:
                        s_secondary = rn.choice(pop.members)

                    # select c_prime as the city following c in s_secondary
                    try:
                        c_prime = s_secondary.solution[s_prime.solution.index(c) + 1]
                    except:
                        c_prime = s_secondary.solution[0]

                # if the surrounding cities of city c in s_prime is c_prime
                i = s_prime.solution.index(c) % (len(s_prime.solution) - 1)

                if i <= 0:
                    if s_prime.solution[i + 1] == c_prime or s_prime.solution[len(s_prime.solution) - 1] == c_prime:
                        # exit from repeat loop
                        break
                else:
                    if s_prime.solution[i + 1] == c_prime or s_prime.solution[i - 1] == c_prime:
                        # exit from repeat loop
                        break

                    # otherwise inverse the section from city[c+1] to c_prime in s_prime
                s_prime.solution = inversion(s_prime.solution,
                                             (s_prime.solution.index(c) + 1) % (len(s_prime.solution) - 1),
                                             s_prime.solution.index(c_prime))
                # set c to c_prime
                c = c_prime

            # if eval(s_prime) is better than eval(s), replace s with s_prime
            s_prime.evaluate_fitness()
            if s_prime.fitness < s.fitness:
                pop.members[pop.members.index(s)] = s_prime
        # after each run through of all members in s, increase the generation count.
        generation += 1
        # If there are any that would take an excessively long time to complete (PR2392 and USA13509), output their fitness per some amount of generations to show the improvement.
        # if generation%10 == 0:
        #     pop_fitness_eval = []
        #     for ind in pop.members:
        #         pop_fitness_eval.append(ind.fitness)
        #     result_fitness = sum(pop_fitness_eval)/len(pop_fitness_eval)
        #     print("Cost for generations: {run} for file {file_name}: {cost}".format(run = generation, file_name = "output{num}.txt".format(num = int(sys.argv[1])), cost = result_fitness), file=f)
    pop_fitness_eval = []
    for ind in pop.members:
        pop_fitness_eval.append(ind.fitness)
    result_fitness = sum(pop_fitness_eval)/len(pop_fitness_eval)

	# # return the resulting population
    return pop


# Run it on each instance of EIL51, EIL76, EIL101, ST70, KROA100, KROC100, LIN105,
# PCB442, PR2392, and USA13509 with a population size of 50, for 20,000 generations 30 times.
tests = ["eil51", "eil76", "eil101", "st70", "kroa100", "kroc100", "lin105", "pcb442", "pr2392", "usa13509"]
with open("output{num}.txt".format(num=int(sys.argv[1])), 'w') as f:
    resulting_populations = []
    filename = "ALL_tsp/{name}.tsp"
    averages = []
    for i in range(30):
        pop = inver_over(0.02, filename.format(name=tests[int(sys.argv[1])]))
        resulting_populations.append(pop)
        fitness = []
        for j in range(len(pop.members)):
            fitness.append(pop.members[j].fitness)
        current_average = sum(fitness)/len(fitness)
        averages.append(current_average)
        print("Cost for run: {run} for file {file_name}: {cost}".format(run = i, file_name = tests[int(sys.argv[1])], cost = current_average), file=f)


    # get average cost and stdev for each resulting population
    avg = sum(averages)/len(averages)
    dev = statistics.stdev(averages)
    print("Average tour cost {file_name}: {cost}".format(file_name=tests[int(sys.argv[1])], cost=avg), file=f)
    print("Standard deviation {file_name}: {cost}".format(file_name=tests[int(sys.argv[1])], cost=dev), file=f)
    print("--- %s minutes taken ---" % ((time.time() - start_time)/60))
    print("\n", file=f)