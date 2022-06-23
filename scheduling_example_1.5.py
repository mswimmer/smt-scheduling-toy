#!/usr/bin/python
""" scheduling_example_1.5

Similar to scheduling_example_1.4 but now we don't allow consecutive shifts

"""

from z3 import Solver, BoolVector, AtLeast, AtMost, And, Not
from print_all_solutions import get_all_solutions

s = Solver()
n_shifts = 16
n_heralds = 8
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

# for every herald, we make sures/he has no consecutive shifts
for i_herald in range(n_heralds):
    for i_shift in range(n_shifts-1):
        s.add(Not(And(herald_shift[i_herald][i_shift],herald_shift[i_herald][i_shift+1])))

#print(s)
results, maxed_out = get_all_solutions(s, 10)
#print(results)

assert len(results) == 10
for result in results:
    print("shift->", end="\t")
    for i_shift in range(n_shifts):
        print("{:4d}".format(i_shift), end="")
    print()
    print("herald", end="\t")
    for i_shift in range(n_shifts):
        print("{:>4s}".format('---'), end="")
    print()
    for i_herald in range(n_heralds):
        print(i_herald, end="\t")
        for i_shift in range(n_shifts):
            print("{:>4s}".format((' ','T')[bool(result.get_interp(herald_shift[i_herald][i_shift]))]), end="")
        print()
    print()
