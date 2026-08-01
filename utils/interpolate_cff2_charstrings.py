
def interpolate_cff2_charstrings(topDict, interpolateFromDeltas, glyphOrder):
    charstrings = topDict.CharStrings
    for gname in glyphOrder:
        # Interpolate charstring
        # e.g replace blend op args with regular args,
        # and use and discard vsindex op.
        charstring = charstrings[gname]
        new_program = []
        vsindex = 0
        last_i = 0
        for i, token in enumerate(charstring.program):
            if token == "vsindex":
                vsindex = charstring.program[i - 1]
                if last_i != 0:
                    new_program.extend(charstring.program[last_i : i - 1])
                last_i = i + 1
            elif token == "blend":
                num_regions = charstring.getNumRegions(vsindex)
                numMasters = 1 + num_regions
                num_args = charstring.program[i - 1]
                # The program list starting at program[i] is now:
                # ..args for following operations
                # num_args values  from the default font
                # num_args tuples, each with numMasters-1 delta values
                # num_blend_args
                # 'blend'
                argi = i - (num_args * numMasters + 1)
                end_args = tuplei = argi + num_args
                while argi < end_args:
                    next_ti = tuplei + num_regions
                    deltas = charstring.program[tuplei:next_ti]
                    delta = interpolateFromDeltas(vsindex, deltas)
                    charstring.program[argi] += otRound(delta)
                    tuplei = next_ti
                    argi += 1
                new_program.extend(charstring.program[last_i:end_args])
                last_i = i + 1
        if last_i != 0:
            new_program.extend(charstring.program[last_i:])
            charstring.program = new_program

