import random as rand
from Individual  import Individual


def ordercrossover(P1, P2):
    # create an empty child list the same size as n
    len1 = len(P1)
    child1 = [0] * len1

    # generate random values for start and end of the arbitrary part
    rand1 = rand.randint(0, len1-1)
    rand2 = rand.randint(0, len1-1)

    # trying min and max functions to easily assign the right values to arbitrary part
    p1_start = min(rand1, rand2)
    p1_end = max(rand1, rand2)

    # copy the arbitrary part over to the child
    for m in range(p1_start, p1_end + 1):
        child1[m] = P1[m]
    # keep a track of the position at which the next allele is to be added in child
    current_c1_pos = p1_end + 1
    # compare the elements that are in p2 with those in child
    # for every element that doesn't already exist in child copy that element over to the spaces after the arbit part
    for i in range(p1_end + 1, len1):
        if P2[i] not in child1:
            child1[current_c1_pos] = P2[i]
            current_c1_pos = current_c1_pos + 1

    # start a new counter for is the end of child 1 has been filled
    new_c1_pos = 0
    # if you reach of of p2 then go back to start but make sure you fill in child to its end
    for j in range(0, len1 ):
        if P2[j] not in child1:
            if current_c1_pos < len1:
                child1[current_c1_pos] = P2[j]
                current_c1_pos = current_c1_pos + 1
            elif current_c1_pos == len1:
                child1[new_c1_pos] = P2[j]
                new_c1_pos = new_c1_pos + 1
    return child1

