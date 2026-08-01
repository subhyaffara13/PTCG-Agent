
def get_lines(command: list[str]) -> list[str]:
    """Run a command and return lines of output

    :param str command: the command to run
    :returns: list of whitespace-stripped lines output by command
    """
    stdout = get_output(command)
    return [line.strip() for line in stdout.splitlines()]


def get_lines(ex, index_type):
    """
    Returns ``(lines, traces, rest)`` for an index type,
    where ``lines`` is the list of list of positions of a matrix line,
    ``traces`` is the list of list of traced matrix lines,
    ``rest`` is the rest of the elements of the tensor.
    """
    def _join_lines(a):
        i = 0
        while i < len(a):
            x = a[i]
            xend = x[-1]
            xstart = x[0]
            hit = True
            while hit:
                hit = False
                for j in range(i + 1, len(a)):
                    if j >= len(a):
                        break
                    if a[j][0] == xend:
                        hit = True
                        x.extend(a[j][1:])
                        xend = x[-1]
                        a.pop(j)
                        continue
                    if a[j][0] == xstart:
                        hit = True
                        a[i] = reversed(a[j][1:]) + x
                        x = a[i]
                        xstart = a[i][0]
                        a.pop(j)
                        continue
                    if a[j][-1] == xend:
                        hit = True
                        x.extend(reversed(a[j][:-1]))
                        xend = x[-1]
                        a.pop(j)
                        continue
                    if a[j][-1] == xstart:
                        hit = True
                        a[i] = a[j][:-1] + x
                        x = a[i]
                        xstart = x[0]
                        a.pop(j)
                        continue
            i += 1
        return a

    arguments = ex.args
    dt = {}
    for c in ex.args:
        if not isinstance(c, TensExpr):
            continue
        if c in dt:
            continue
        index_types = c.index_types
        a = []
        for i in range(len(index_types)):
            if index_types[i] is index_type:
                a.append(i)
        if len(a) > 2:
            raise ValueError('at most two indices of type %s allowed' % index_type)
        if len(a) == 2:
            dt[c] = a
    #dum = ex.dum
    lines = []
    traces = []
    traces1 = []
    #indices_to_args_pos = ex._get_indices_to_args_pos()
    # TODO: add a dum_to_components_map ?
    for p0, p1, c0, c1 in ex.dum_in_args:
        if arguments[c0] not in dt:
            continue
        if c0 == c1:
            traces.append([c0])
            continue
        ta0 = dt[arguments[c0]]
        ta1 = dt[arguments[c1]]
        if p0 not in ta0:
            continue
        if ta0.index(p0) == ta1.index(p1):
            # case gamma(i,s0,-s1) in c0, gamma(j,-s0,s2) in c1;
            # to deal with this case one could add to the position
            # a flag for transposition;
            # one could write [(c0, False), (c1, True)]
            raise NotImplementedError
        # if p0 == ta0[1] then G in pos c0 is mult on the right by G in c1
        # if p0 == ta0[0] then G in pos c1 is mult on the right by G in c0
        ta0 = dt[arguments[c0]]
        b0, b1 = (c0, c1) if p0 == ta0[1]  else (c1, c0)
        lines1 = lines.copy()
        for line in lines:
            if line[-1] == b0:
                if line[0] == b1:
                    n = line.index(min(line))
                    traces1.append(line)
                    traces.append(line[n:] + line[:n])
                else:
                    line.append(b1)
                break
            elif line[0] == b1:
                line.insert(0, b0)
                break
        else:
            lines1.append([b0, b1])

        lines = [x for x in lines1 if x not in traces1]
        lines = _join_lines(lines)
    rest = []
    for line in lines:
        for y in line:
            rest.append(y)
    for line in traces:
        for y in line:
            rest.append(y)
    rest = [x for x in range(len(arguments)) if x not in rest]

    return lines, traces, rest

