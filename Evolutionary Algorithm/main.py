# Written by Lelep Wighton for Evolutionary Computation 2021, Assignment 1 Group 1

# Import the modules used to create evolutionary algorithms
from ParseNodeFile import *
from Population import Population
from edge import *
from selection import *
from Tournament_Selection import *
from ordercrossover import *
from cyclecrossover import *
from PMX import *
from Mutation import *
import copy as cp


# This function drives all the action, based on user input.
def main():
    # Set debug level:
    #   0: Only Essential Messages
    #   1: Print fitness every hundred generations, print generations of interest at end
    #   2: Print everything
    debug = 1

    # Loop until manually exited from within to get a valid file
    while True:
        # Read the desired TSP file name from user
        file_location = input("Enter TSP file name: ")
        # Append "ALL_tsp/" if not already present. Code expects test cases to be in a sub-folder.
        if file_location[0:7] != "ALL_tsp/":
            file_location = "ALL_tsp/" + file_location
        if file_location[len(file_location)-1] != "p":
            file_location = file_location + ".tsp"

        # Safely retrieve nodes from file
        try:
            # Try to retrieve the nodes from the specified location
            nodes = parse_node_file(file_location)
            # If successful, exit loop
            break
        except IOError:
            print("Invalid file name, try again")

    # Loop until valid pop size given
    while True:
        # Safely retrieve integer from user
        try:
            # Try to retrieve a string from the user and parse it to an int
            pop_size = int(input("Enter Population Size: "))
            # If successful, exit loop
            break
        except ValueError:
            print("Not an integer, try again")

    # Loop until valid generation counts given
    while True:
        # Safely retrieve integer from user
        try:
            # Read in a space-separated string of integers
            line = input("Enter Generation breakpoints, space-separated: ")
            # Split line by spaces
            gen_strings = line.split()
            # Initialise gen_breaks
            gen_breaks = []

            # Loop over the split line, converting to int and appending to the generation breakpoints
            for string in gen_strings:
                # Convert the string to an int, and add it to the list
                gen_breaks.append(int(string))

            # As a sanity check, sort the list into ascending order
            gen_breaks.sort()

            # If successful, exit loop
            break
        except ValueError:
            print("Not an integer, try again")

    # Ask User Whether they want to use a preset algorithm or manually input one.
    try:
        # Try to retrieve a string from the user and parse it to an int
        algorithm = int(input("Enter Desired Algorithm: (1), (2), (3), anything else for manual input: "))
    except ValueError:
        algorithm = -1

    # If the algorithm specified matches the first, use the given inputs
    if algorithm == 1:
        parent_selection = "Fitness-Proportional"
        crossover = "Edge"
        mutation_style = "Swap"
        survivor_selection = "Elitism"
    elif algorithm == 2:
        parent_selection = "Fitness-Proportional"
        crossover = "Edge"
        mutation_style = "Scramble"
        survivor_selection = "Elitism"
    elif algorithm == 3:
        parent_selection = "Tournament"
        replacement_p = True
        tourney_size_p = 2
        win_rate_p = 0.8
        crossover = "Edge"
        mutation_style = "Swap"
        survivor_selection = "Elitism"
    else:
        # Retrieve parent selection method
        # Checks the first character, and sets to a standard form.
        # This should give more flexibility for errors and capitalisation variation.
        while True:
            print("Parent Selection Methods: Elitism, Fitness-Proportional, Tournament.")
            parent_selection = input("Enter desired Parent Selection Method: ")

            # If start matches elitism, set to elitism and exit loop
            if (parent_selection[0] == 'e') | (parent_selection[0] == 'E'):
                parent_selection = "Elitism"
                break
            # If start matches Fitness-proportional set to fitness proportional and exit loop
            elif (parent_selection[0] == 'f') | (parent_selection[0] == 'F'):
                parent_selection = "Fitness-Proportional"
                break
            # If start matches Tournament, set to Tournament and exit loop
            elif (parent_selection[0] == 't') | (parent_selection[0] == 'T'):
                # Try to safely receive tournament parameters
                while True:
                    try:
                        replacement_p = input("Allow individuals to compete in multiple matches?\nY / N (default) :")
                        # Set replacement to true if Y, false otherwise
                        if (replacement_p == 'y') | (replacement_p == 'Y'):
                            replacement_p = True
                        else:
                            replacement_p = False
                        tourney_size_p = int(input("Enter desired number of participants in each match: "))
                        win_rate_p = float(input("Enter the chance of the best entrant winning (between 0 and 1): "))

                        # Tidy the given input
                        parent_selection = "Tournament"
                        # Exit the parent selection style loop
                        break
                    except ValueError:
                        print("Please enter a valid number")
                # Exit the selection style loop
                break

        # Retrieve crossover style
        # Checks the first character, and sets to a standard form.
        # This should give more flexibility for errors and capitalisation variation.
        while True:
            print("Crossover Methods: Order, Partially-Mapped Crossover (PMX), Cycle, Edge, None.")
            crossover = input("Enter desired crossover Method: ")

            # If start matches Order, set to Order and exit loop
            if (crossover[0] == 'o') | (crossover[0] == 'O'):
                crossover = "Order"
                break
            # If start matches PMX set to fitness PMX and exit loop
            elif (crossover[0] == 'p') | (crossover[0] == 'P'):
                crossover = "PMX"
                break
            # If start matches Cycle, set to Cycle and exit loop
            elif (crossover[0] == 'c') | (crossover[0] == 'C'):
                crossover = "Cycle"
                break
            # If start matches Edge, set to Edge and exit loop
            elif (crossover[0] == 'e') | (crossover[0] == 'E'):
                crossover = "Edge"
                break
            # If start matches None, set to None and exit loop
            elif (crossover[0] == 'n') | (crossover[0] == 'N'):
                crossover = "None"
                break

        # Retrieve Mutation style
        # Checks the first few characters, and sets to a standard form.
        # This should give more flexibility for errors and capitalisation variation.
        while True:
            print("Mutation Methods: Insert, Swap, Inversion, Scramble, None.")
            mutation_style = input("Enter desired mutation Method: ")

            # If first letter is 'i', but length is less than 3, retry
            if (len(mutation_style) < 3) & ((mutation_style[0] == 'i') | (mutation_style[0] == 'I')):
                continue
            # If first letter is 's', but length is less than 22, retry
            if (len(mutation_style) < 2) & ((mutation_style[0] == 's') | (mutation_style[0] == 'S')):
                continue
            # If first letter is 'i', discriminate between insert and inversion
            elif (mutation_style[0] == 'i') | (mutation_style[0] == 'I'):
                # If start matches Insert, set to Insert and exit loop
                if (mutation_style[2] == 's') | (mutation_style[2] == 'S'):
                    mutation_style = "Insert"
                    break
                # If start matches Inversion, set to Cycle and exit loop
                elif (mutation_style[0] == 'i') | (mutation_style[0] == 'I'):
                    mutation_style = "Inversion"
                break
            # If first letter is 's', discriminate between swap and scramble
            elif (mutation_style[0] == 's') | (mutation_style[0] == 'S'):
                # If start matches Swap set to fitness Swap and exit loop
                if (mutation_style[1] == 'w') | (mutation_style[1] == 'W'):
                    mutation_style = "Swap"
                    break
                # If start matches Edge, set to Edge and exit loop
                elif (mutation_style[1] == 'c') | (mutation_style[1] == 'C'):
                    mutation_style = "Scramble"
                    break
            # If start matches None, set to None and exit loop
            elif (mutation_style[0] == 'n') | (mutation_style[0] == 'N'):
                mutation_style = "None"
                break

        # Retrieve survivor selection style
        # Checks the first character, and sets to a standard form.
        # This should give more flexibility for errors and capitalisation variation.
        while True:
            print("Survivor Selection Methods: Elitism, Fitness-Proportional, Tournament, Children Only.")
            survivor_selection = input("Enter desired Survivor Selection Method: ")

            # If start matches elitism, set to elitism and exit loop
            if (survivor_selection[0] == 'e') | (survivor_selection[0] == 'E'):
                survivor_selection = "Elitism"
                break
            # If start matches Fitness-proportional set to fitness proportional and exit loop
            elif (survivor_selection[0] == 'f') | (survivor_selection[0] == 'F'):
                survivor_selection = "Fitness-Proportional"
                break
            # If start matches Tournament, set to Tournament and exit loop
            elif (survivor_selection[0] == 't') | (survivor_selection[0] == 'T'):
                # Try to safely receive tournament parameters
                while True:
                    try:
                        replacement_s = input("Allow individuals to compete in multiple matches?\nY / N (default) :")
                        # Set replacement to true if Y, false otherwise
                        if (replacement_s == 'y') | (replacement_s == 'Y'):
                            replacement_s = True
                        else:
                            replacement_s = False

                        tourney_size_s = int(input("Enter desired number of participants in each match: "))
                        win_rate_s = float(input("Enter the chance of the best entrant winning (between 0 and 1): "))
                        survivor_selection = "Tournament"
                        # Exit the tournament parameter loop
                        break
                    except ValueError:
                        print("Please enter a valid number")
                    # Exit the selection style loop
                    break
            # If start matches Children Only set to Children Only and exit loop
            elif (survivor_selection[0] == 'c') | (survivor_selection[0] == 'C'):
                survivor_selection = "Children Only"
            break

    # TEST: print location and nodes
    if debug == 2:
        print_nodes(nodes)
        print(file_location)
        print(pop_size)
        print(gen_breaks)
        print(parent_selection)
        print(crossover)
        print(mutation_style)
        print(survivor_selection)

    # Create a population using the given nodes and pop size.
    pop = Population(pop_size, nodes)

    # initialise list to store the fitness at the desired generations
    generation_fitness = []

    for generation in range(gen_breaks[-1]):
        # Perform Parent Selection
        # Initialise list of children
        children = []

        # If crossover is set to none, make the children a deep copy of the parents.
        if crossover == "None":
            children = cp.deepcopy(pop).members
        # Otherwise build up the children through parent selection, crossover and mutation
        else:
            # Loop up to pop_size
            for i in range(pop_size):
                # Perform parent selection
                # If parent_selection is Elitism, use it to select two parents
                # Note: This will always result in the same two parents
                if parent_selection == "Elitism":
                    parents = elitism_selection(pop, 2)
                # otherwise, if Selection is Fitness-Proportional, use it to select two parents
                elif parent_selection == "Fitness-Proportional":
                    parents = fitness_proportional_selection(pop, 2)
                # otherwise, if Selection is Tournament, use it to select two parents
                elif parent_selection == "Tournament":
                    parents = tournament_selection(pop, win_rate_p, tourney_size_p, replacement_p, 2)
                # Otherwise, print error and exit.
                else:
                    print("Unexpected parent selection method")
                    # This is just to convince my IDE that parents is assigned before reference. -_-
                    parents = [pop.members[0], pop.members[0]]
                    exit(1)

                # Test: Print out parent pairs
                if debug == 2:
                    print(parents[0].solution, "\n", parents[1].solution, "\n")

                # Now that we have two parents, cross them over and append the results to child
                # Use Order if selected
                if crossover == "Order":
                    # Append the order-child to the children
                    child_sol = ordercrossover(parents[0].solution, parents[1].solution)
                # Use PMX if selected
                elif crossover == "PMX":
                    # Append the PMX-child to the children
                    child_sol = PMX_crossover(parents[0].solution, parents[1].solution)
                # Use Cycle if selected
                elif crossover == "Cycle":
                    # Append the Cycle-child to the children
                    child_sol = cyclecrossover(parents[0].solution, parents[1].solution)
                # Use Edge if selected
                elif crossover == "Edge":
                    # Append the Edge-child to the children
                    child_sol = edge_crossover(parents[0].solution, parents[1].solution)
                # Otherwise, print error and exit.
                else:
                    print("Unexpected Crossover method")
                    # This is just to convince my IDE that child is assigned before reference. -_-
                    child_sol = pop.members[0]
                    exit(1)

                # Create a new individual to hold the child
                child = Individual(nodes)
                # Set the child's fitness to child_sol and update fitness
                child.solution = child_sol
                child.evaluate_fitness()

                # Test: Print out crossover child
                if debug == 2:
                    print("Crossover child: ", child.solution, ", fitness: ", child.fitness)

                # Now that we have a child, we need to mutate it. Don't take that out of context.
                if (mutation_style == "Insert") | (mutation_style == "Inversion") | (mutation_style == "Swap") \
                        | (mutation_style == "Scramble"):
                    child.solution = mutation(child.solution, mutation_style)
                else:
                    # Print a warning if mutation not set to None
                    if mutation_style != "None":
                        print("Unexpected mutation method! Doing nothing instead")
                    # Otherwise, do nothing

                # Test: Print Child's old fitness
                if debug == 2:
                    print(child.fitness)

                # Now that the child has been crossed over and mutated, reevaluate its fitness
                child.evaluate_fitness()

                # Test: Print child's new fitness
                if debug == 2:
                    print(child.fitness)

                # Finally, append child to children
                children.append(child)
        # Now we should have a child population in children that is as large as the main population.

        # Test: Retrieve the fittest member by running elitism for size 1
        fittest_member = elitism_selection(pop, 1)[0]
        # Test: print fitness of best solution
        if debug == 2:
            print("Fitness of fittest member before:", fittest_member.fitness)

        # If survivor_selection is Children Only, set survivors to children
        if survivor_selection == "Children Only":
            survivors = children
        # Otherwise, use the selected algorithm
        else:
            # Add the children to the population
            pop.members.extend(children)

            # Run survivor selection to populate new population
            # if Selection is Elitism, use it to select survivors
            if survivor_selection == "Elitism":
                survivors = elitism_selection(pop, pop_size)
            # otherwise, if Selection is Fitness-Proportional, use it to select survivors
            elif survivor_selection == "Fitness-Proportional":
                survivors = fitness_proportional_selection(pop, pop_size)
            # otherwise, if Selection is Tournament, use it to select survivors
            elif survivor_selection == "Tournament":
                survivors = tournament_selection(pop, win_rate_s, tourney_size_s, replacement_s, pop_size)
            # Otherwise, print error and exit.
            else:
                print("Unexpected survivor selection method")
                # This is just to convince my IDE that survivors is assigned before reference. -_-
                survivors = [pop.members[0], pop.members[0]]
                exit(1)

        # Set the population to the new population
        pop.members = survivors

        # Retrieve the fittest member by running elitism for size 1
        fittest_member = elitism_selection(pop, 1)[0]

        # If generation is a break, record the fitness
        if (generation + 1) in gen_breaks:
            generation_fitness.append(fittest_member)

        # Test: print fitness of best solution
        if ((debug == 1) & ((generation+1) % 100 == 0)) | ((generation+1) in gen_breaks):
            print("Fitness at ", generation+1, "th generation:", fittest_member.fitness)

    # Finally, if Debug was one, print out the fitness at the gen breaks at the end
    if debug == 1:
        print("\n\n")
        for i in range(len(gen_breaks)):
            print("Fitness at ", gen_breaks[i], "th generation:", generation_fitness[i].fitness)


# Apparently Python needs this for some reason.
if __name__ == '__main__':
    main()
