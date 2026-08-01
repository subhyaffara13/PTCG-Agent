
def _convertBlendOpToArgs(blendList):
    # args is list of blend op args. Since we are supporting
    # recursive blend op calls, some of these args may also
    # be a list of blend op args, and need to be converted before
    # we convert the current list.
    if any([isinstance(arg, list) for arg in blendList]):
        args = [
            i
            for e in blendList
            for i in (_convertBlendOpToArgs(e) if isinstance(e, list) else [e])
        ]
    else:
        args = blendList

    # We now know that blendList contains a blend op argument list, even if
    # some of the args are lists that each contain a blend op argument list.
    # 	Convert from:
    # 		[default font arg sequence x0,...,xn] + [delta tuple for x0] + ... + [delta tuple for xn]
    # 	to:
    # 		[ [x0] + [delta tuple for x0],
    #                 ...,
    #          [xn] + [delta tuple for xn] ]
    numBlends = args[-1]
    # Can't use args.pop() when the args are being used in a nested list
    # comprehension. See calling context
    args = args[:-1]

    l = len(args)
    numRegions = l // numBlends - 1
    if not (numBlends * (numRegions + 1) == l):
        raise ValueError(blendList)

    defaultArgs = [[arg] for arg in args[:numBlends]]
    deltaArgs = args[numBlends:]
    numDeltaValues = len(deltaArgs)
    deltaList = [
        deltaArgs[i : i + numRegions] for i in range(0, numDeltaValues, numRegions)
    ]
    blend_args = [a + b + [1] for a, b in zip(defaultArgs, deltaList)]
    return blend_args

