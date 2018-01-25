import time
from z3 import sat, is_array, Z3_UNINTERPRETED_SORT, Or

def get_all_solutions(s, limit = 0):
    result=[]
    while True:
        start_time = time.clock()
        if s.check() == sat:
            m = s.model()
            print("Time for iteration {}: {}".format(len(result), time.clock() - start_time))
            #print(m)
            result.append(m)
            # Create a new constraint the blocks the current model
            block = []
            for d in m:
                # d is a declaration
                if d.arity() > 0:
                    raise Z3Exception("uninterpreted functions are not suppported")
                # create a constant from declaration
                c=d()
                #print c, m[d]
                if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
                    raise Z3Exception("arrays and uninterpreted sorts are not supported")
                block.append(c != m[d])
            #print "new constraint:",block
            s.add(Or(block))
        else:
            print("Number of results", len(result))
            break
        if limit > 0 and len(result) >= limit:
            print("Maxed out at {} results".format(len(result)))
            return result, False
    return result, True
