import sys

def _combine_type1_subsystems(subsystem, funcs, t):
    indices = [i for i, sys in enumerate(zip(subsystem, funcs)) if _is_type1(sys, t)]
    remove = set()
    for ip, i in enumerate(indices):
        for j in indices[ip+1:]:
            if any(eq2.has(funcs[i]) for eq2 in subsystem[j]):
                subsystem[j] = subsystem[i] + subsystem[j]
                remove.add(i)
    subsystem = [sys for i, sys in enumerate(subsystem) if i not in remove]
    return subsystem

