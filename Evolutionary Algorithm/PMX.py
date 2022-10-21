import numpy as np

# to select subset from the parents, it returns the range
def getStartEnd(g1, g2):
    return min(g1, g2), max(g1, g2)


def PMX_crossover(parent1, parent2):
    # returns list
    p1len = len(parent1)
    p2len = len(parent2)
    # pick start and end range to pick generation subset
    start, end = getStartEnd(int(np.random.random_sample() * p1len), int(np.random.random_sample() * p2len))
    successor = [-1] * p1len # successor
    successor[start:end] = parent1[start:end] # extract subset from parent1

    for i, x in enumerate(parent2[start:end]):
        i += start
        if x not in successor:
            while successor[i] != -1:
                i = parent2.index(parent1[i])
            successor[i] = x
    # subset from parent2
    i = 0
    for c in successor:
        if c == -1:
            successor[i] = parent2[i]
        i = i + 1
    return successor
