# Written by Sebastian Trenberth for Evolutionary Computation 2021, Assignment 1 Group 1

import random as rn


def fit(ind):
    return ind.fitness


def determ(rate, slot):
    if rn.random() <= rate:
        return slot
    else:
        return determ(rate, slot + 1)


def tournament_selection(population, rate, tourney_size, replacement, rounds):

    selected_ind = []
    for r in range(rounds):
        # choose tourney_size participants
        participants = rn.choices(population.members,  k = tourney_size)

        # sort into fitness order
        participants.sort(key=fit)

        # find which participant wins
        slot = determ(rate, 0)

        # error catching
        if slot > len(participants)-1:
            slot = len(participants)-1

        # append the winner to the resulting population (can be survivors or parents)
        selected_ind.append(participants[slot])

        # check if the winner needs to be removed from available pool
        if not replacement:
            population.members.remove(participants[slot])

    return selected_ind