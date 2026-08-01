
def _component_division(eqs, funcs, t):

    # Assuming that each eq in eqs is in canonical form,
    # that is, [f(x).diff(x) = .., g(x).diff(x) = .., etc]
    # and that the system passed is in its first order
    eqsmap, eqsorig = _eqs2dict(eqs, funcs)

    subsystems = []
    for cc in connected_components(_dict2graph(eqsmap)):
        eqsmap_c = {f: eqsmap[f] for f in cc}
        sccs = strongly_connected_components(_dict2graph(eqsmap_c))
        subsystem = [[eqsorig[f] for f in scc] for scc in sccs]
        subsystem = _combine_type1_subsystems(subsystem, sccs, t)
        subsystems.append(subsystem)

    return subsystems

