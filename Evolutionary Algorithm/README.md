# EC-Assignment01
Created by the following people for Evolutionary Computation, Semester 2 2021: 
* Lelep Wighton, 1630177, 
[lelep.wighton@student.adelaide.edu.au](lelep.wighton@student.adelaide.edu.au)
* Daniel Harris, a1749892, 
[daniel.harris@student.adelaide.edu.au](daniel.harris@student.adelaide.edu.au)
* Jia Jun Loucas Chai, a1755688, 
[a1755688@student.adelaide.edu.au](a1755688@student.adelaide.edu.au)
* Farishta Hashimi, a1792172, 
[farishta.hashimi@student.adelaide.edu.au](farishta.hashimi@student.adelaide.edu.au)
* Ulugbek Kakhkhorov, a1801921, 
[ulugbek.kakhkhorov@student.adelaide.edu.au](ulugbek.kakhkhorov@student.adelaide.edu.au)
* Sebastian Trenberth, a1747809,
[sebastian.trenberth@student.adelaide.edu.au](sebastian.trenberth@student.adelaide.edu.au)

In addition to checking out the GitHub Repository, you need to 
Download ALL_tsp.tar.gz, and extract the files within, so that 
the folder All_tsp is stored in the same directory as the code.
Our code expects the tsp files to be stored in ./ALL_tsp/filename.

The python interpreter we used was Python 3.9, which you should 
use to run main.py. When you run it, it will begin taking input.
In general, any invalid inputs will cause it to repeat the prompt, 
possibly with an elaborating error message.

## Main
First you should enter the filename of the desired test case. 
Both "ALL_tsp/" and ".tsp" are can be safely omitted when 
referencing files, for convenience. There is currently no way of using a 
tsp file not in ./ALL_tsp.

Next it will ask you for the population size. This should be an integer.

Next you will be asked for the breakpoints: the generations at which
you wish to know the fitness. This should be a space-separated list
of integers, which will be sorted even if given in the wrong order.

You will then be asked what algorithm you wish to run, if any. See
the attached pdf for the details of the three algorithms. 
Enter the integers "1", "2", or "3" for the corresponding algorithm,
or give any other input to manually specify the parameters. 
If an algorithm is selected, the code will begin to run, while if not,
further information will be requested.

If you select manual specification, you will then be asked to input the parent 
selection style. If tournament selection is selected, you will also be asked
to specify whether replacement is being used (Enter 'y' or 'Y' to
allow replacement, and anything else to disallow it), the tourney
size (an integer), and the win rate (a float, 0 < win_rate <= 1. Currently not validity-checked.). 
You must give a valid answer to all three to proceed.

After that, you will be asked to specify the crossover and mutation styles, or 
"None" if undesired, followed by the survivor selection, 
which is in the same format as the parent selection.

When the code executes, it will print out the fitness every hundred
generations to indicate progress, before printing out the fitness at each
of the generation breakpoints when complete.

## Inver-Over
Inver-Over has functionality to run the 10 tests expected in the assignment, with populations of 50, generation size of 20,000 and 30 runthroughs. It expects a single command line argument in the form of an integer between 0 and 9, which will choose a test case based on the order in which they appear.

To execute, the command:

  python inver_over.py n
  
will run it with the nth test case, indexed from 0, in the order that they are supplied in the assignment specifications.
