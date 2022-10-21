# edge recombination
import numpy as np


def edge_crossover(parent1, parent2):
    # get parent length
    p1len = len(parent1)
    p2len = len(parent2)

    p2 = []
    # get subset from generation (mix parent1,parent2 subsets)
    generation1 = int(np.random.random_sample()*p1len)
    generation2 = int(np.random.random_sample()*p2len)
    end = max(generation1,generation2)
    start = min(generation1, generation2)
    current = [parent1[i] for i in range(start,end+1)]# get subset from parent1

    i = end+1
    current = sorted(current)# sort current individual
    while i < (end + p1len + 1):# iteration
        index = i
        if index >= p1len:
            index -= p1len
        if parent2[index] not in current:# parent2 not in current subset
            p2.append(parent2[index])
        i = i + 1
    successor = p2[p2len - end:] + current + p2[:p2len - end]
    return successor