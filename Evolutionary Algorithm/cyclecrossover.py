from Individual import Individual


# this function creates the cycles by taking Parent lists and a starting point
def cycles(P1, P2, cycle_start):
    # indexes are changed according to Parent 1
    # index of the cycle is initialised to be the index of the starting point
    p1_index = P1.index(cycle_start)

    # the label contains the values which are visited or belong to the current cycle
    p2_label = cycle_start

    # initialise list to contain the indexes of the cycle
    cycle_index_list = []

    # to keep track of where the cycle ends this is updated once the loop starts
    cycle_end = 0

    # as long as we don't reach the element at the start of the cycle the loop increments
    while p2_label != cycle_end:
        cycle_end = cycle_start
        # everytime a new allele in P1 is visited the index is appended to the index list
        cycle_index_list.append(p1_index)
        # the label variable containing the values at the visited indexes changes with respect to P2
        # each value is first visited in P2 therefore, P2 governs this variables changes
        p2_label = P2[p1_index]
        # once a new value in P2 is visited it is then looked for in P1 ( as a rule of the cycle crossover)
        # the index of that new value is found in P1 and therefore the index is updated everytime-
        # a new allele in P1 is visited
        p1_index = P1.index(p2_label)
        # then the list containing the order and indexes visited is returned
    return cycle_index_list


def cyclecrossover(P1, P2):
    length_p = len(P1)
    # initialise a child list
    child1 = [0] * length_p

    # initialise lists to contain the indexes of the labels in Parents from each cycle
    # cycle_1_indexes will contain cycles belonging to P1 (the odd cycles)
    cycle1_indexes = []
    # cycle2_indexes will contain cycles belonging to P2
    cycle2_indexes = []

    # by default cycle 1 would always start at the first unvisited value of P1 which is at index 0
    cycle1_start = P1[0]

    # to keep count of which cycle number it is at, for odd cycles P1 order is copied and for even cycles P2
    cycle_num_count = 0

    # a while loop that will generate cycles for as long is there are unvisited values in P1
    # a track of the unvisited values of P is kept by checking if child still has any 0 left in its list
    while cycle1_start != -1:

        # if we are at an odd cycle it will copy the values to cycle1
        if (cycle_num_count % 2) == 0:
            cycle1_indexes = cycles(P1, P2, cycle1_start)
            cycle_num_count = cycle_num_count + 1

        # if we are at an even cycle it will copy the values cycle2
        elif (cycle_num_count % 2) != 0:
            cycle2_indexes = (cycles(P1, P2, cycle1_start))
            cycle_num_count = cycle_num_count + 1

        # uncomment to see if copied correctly
        # print('cycle1: ', cycle1_indexes)
        # print('cycle2: ', cycle2_indexes)

        # if the cycles have values in them/ which ever one that has values in them it will copy those to child
        if len(cycle1_indexes) != 0:
            for i in range(len(cycle1_indexes)):
            # the values in each index of cycle1_indexes act as an index guid for copying in the right order
                child1[cycle1_indexes[i]] = P1[cycle1_indexes[i]]

        if len(cycle2_indexes) != 0:
            for j in range(len(cycle2_indexes)):
                child1[cycle2_indexes[j]] = P2[cycle2_indexes[j]]

        # after each cycle the next unvisited value is found
        for i in range(0, length_p):
            if P1[i] not in child1:
                cycle1_start = P1[i]
                break
            # if end of loop is reached and the value of cycle_start is already in child then set the start
            # to -1 to end the while loop
            # this means that we couldn't find an unvisited values
            elif (i == length_p-1) and (child1.count(cycle1_start) > 0):
                cycle1_start = -1
        # as a precautionary step in case there is for any reason a chance for infinit loop
        # the lines bellow are used to avoid this outcome
        if child1.count(0) == 0:
            cycle1_start = -1

        # index lists are emptied for the next loop
        cycle1_indexes = []
        cycle2_indexes = []

    return child1
