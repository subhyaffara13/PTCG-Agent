
def _convertToBlendCmds(args):
    # return a list of blend commands, and
    # the remaining non-blended args, if any.
    num_args = len(args)
    stack_use = 0
    new_args = []
    i = 0
    while i < num_args:
        arg = args[i]
        i += 1
        if not isinstance(arg, list):
            new_args.append(arg)
            stack_use += 1
        else:
            prev_stack_use = stack_use
            # The arg is a tuple of blend values.
            # These are each (master 0,delta 1..delta n, 1)
            # Combine as many successive tuples as we can,
            # up to the max stack limit.
            num_sources = len(arg) - 1
            blendlist = [arg]
            stack_use += 1 + num_sources  # 1 for the num_blends arg

            # if we are here, max stack is the CFF2 max stack.
            # I use the CFF2 max stack limit here rather than
            # the 'maxstack' chosen by the client, as the default
            # maxstack may have been used unintentionally. For all
            # the other operators, this just produces a little less
            # optimization, but here it puts a hard (and low) limit
            # on the number of source fonts that can be used.
            #
            # Make sure the stack depth does not exceed (maxstack - 1), so
            # that subroutinizer can insert subroutine calls at any point.
            while (
                (i < num_args)
                and isinstance(args[i], list)
                and stack_use + num_sources < maxStackLimit
            ):
                blendlist.append(args[i])
                i += 1
                stack_use += num_sources
            # blendList now contains as many single blend tuples as can be
            # combined without exceeding the CFF2 stack limit.
            num_blends = len(blendlist)
            # append the 'num_blends' default font values
            blend_args = []
            for arg in blendlist:
                blend_args.append(arg[0])
            for arg in blendlist:
                assert arg[-1] == 1
                blend_args.extend(arg[1:-1])
            blend_args.append(num_blends)
            new_args.append(blend_args)
            stack_use = prev_stack_use + num_blends

    return new_args

