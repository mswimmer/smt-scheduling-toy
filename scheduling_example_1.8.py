#!/usr/bin/python
""" scheduling_example_1.8

Similar to scheduling_example_1.7 but now certain heralds have preferences

"""

from z3 import Solver, BoolVector, AtLeast, AtMost, Not, Or
from print_all_solutions import get_all_solutions

s = Solver()
n_shifts = 16
n_heralds = 8
n_days = 4
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

# for every herald, we make sures/he has only one shift per day
for i_herald in range(n_heralds):
    # TODO: this obviously will fail for n_shifts not cleanly divisible through 4
    for i_day in range(n_days):
        s.add(AtMost(
            *[herald_shift[i_herald][int(n_shifts/n_days)*i_day + i] for i in range(int(n_shifts/n_days)) ],
            1))

s.add(herald_shift[0][0] == True)
s.add(herald_shift[0][n_shifts-1] == True)

morning_shifts = [0, 1, 4, 5, 8, 9, 12, 13]
afternoon_shifts = [2, 3, 6, 7, 10, 11, 14, 15]

# heralds 1 and 2 want to avoid the morning shifts
s.add(Not(Or([herald_shift[1][i_shift] == True for i_shift in morning_shifts])))
s.add(Not(Or([herald_shift[2][i_shift] == True for i_shift in morning_shifts])))
# heralds 3 and 4 want to avoid the afternoon shifts
s.add(Not(Or([herald_shift[3][i_shift] == True for i_shift in afternoon_shifts])))
s.add(Not(Or([herald_shift[4][i_shift] == True for i_shift in afternoon_shifts])))

# herald 5 can only make it on the first two days
s.add(Not(Or([herald_shift[5][i_shift] == True for i_shift in range(int(n_shifts/2), n_shifts)])))

print(s)
results, maxed_out = get_all_solutions(s, 50)

assert len(results) == 50
for result in results:
    print("day->", end="\t")
    for i_shift in range(n_shifts):
        print("{:4d}".format(int(i_shift/n_days)), end="")
    print()
    print("", end="\t")
    for i_shift in range(n_shifts):
        print("{:>4}".format(('pm', 'am')[i_shift%n_days < 2] ), end="")
    print()
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
