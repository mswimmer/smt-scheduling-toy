#!/usr/bin/python
from z3 import Solver, IntVector, Sum, Or
from print_all_solutions import get_all_solutions

s = Solver()
n_shifts = 4
n_heralds = 2
n_shift_max = 2

# create the herald matrix
herald_shifts = []
for i in range(n_heralds):
    herald_shifts.append(IntVector('herald_'+str(i)+'_shifts', n_shifts))
# ensure that for each herald and shift, the herald can only have one shift
# this is the negative consequence of using Ints instead of Bools
for i_herald in range(n_heralds):
    for i_shift in range(n_shifts):
        s.add(Or(herald_shifts[i_herald][i_shift] == 0, herald_shifts[i_herald][i_shift] == 1))
    
#for every shift, count the number of heralds assigned to it and ensure it's one
for i_shift in range(n_shifts):
    s.add(Sum([herald_shifts[i_herald][i_shift] for i_herald in range(n_heralds)]) == 1)

# for every herald, we need to make sure s/he has exactly 2 shifts
for i_herald in range(n_heralds):
    s.add(Sum(herald_shifts[i_herald]) == 2)

print(s)
results = get_all_solutions(s)
print(results)
