#!/usr/bin/python
""" Similar to scheduling_example_1.1 but with BoolVectors """

from z3 import *
from print_all_solutions import get_all_solutions

s = Solver()
n_shifts = 4
n_heralds = 2
n_shift_max = 2

# create the herald-shift matrix
herald_shift = []
for i in range(n_heralds):
    herald_shift.append(BoolVector('herald_'+str(i)+'_shift', n_shifts))

#for every shift, count the number of heralds assigned to it and ensure it's one
for i_shift in range(n_shifts):
    # TODO: PbEq Should be able to do this in one pass, but how does it work?
    s.add(AtMost(*([herald_shift[i_herald][i_shift] for i_herald in range(n_heralds)]), 1))
    s.add(AtLeast(*([herald_shift[i_herald][i_shift] for i_herald in range(n_heralds)]), 1))

# for every herald, we need to make sure s/he has exactly 2 shifts
for i_herald in range(n_heralds):
    s.add(AtMost(*herald_shift[i_herald], 2))
    s.add(AtLeast(*herald_shift[i_herald], 2))

print(s)
results = get_all_solutions(s)
print(results)
assert len(results) == 6
