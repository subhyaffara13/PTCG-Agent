
def _input_to_binlist(inputlist, variables):
    binlist = []
    bits = len(variables)
    for val in inputlist:
        if isinstance(val, int):
            binlist.append(ibin(val, bits))
        elif isinstance(val, dict):
            nonspecvars = list(variables)
            for key in val.keys():
                nonspecvars.remove(key)
            for t in product((0, 1), repeat=len(nonspecvars)):
                d = dict(zip(nonspecvars, t))
                d.update(val)
                binlist.append([d[v] for v in variables])
        elif isinstance(val, (list, tuple)):
            if len(val) != bits:
                raise ValueError("Each term must contain {bits} bits as there are"
                                 "\n{bits} variables (or be an integer)."
                                 "".format(bits=bits))
            binlist.append(list(val))
        else:
            raise TypeError("A term list can only contain lists,"
                            " ints or dicts.")
    return binlist

