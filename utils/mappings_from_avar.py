
def mappings_from_avar(font, denormalize=True):
    fvarAxes = font["fvar"].axes
    axisMap = {a.axisTag: a for a in fvarAxes}
    axisTags = [a.axisTag for a in fvarAxes]
    axisIndexes = {a.axisTag: i for i, a in enumerate(fvarAxes)}
    if "avar" not in font:
        return {}, []
    avar = font["avar"]
    axisMaps = {
        tag: seg
        for tag, seg in avar.segments.items()
        if seg and seg != {-1: -1, 0: 0, 1: 1}
    }
    mappings = []

    if getattr(avar, "majorVersion", 1) == 2:
        varStore = avar.table.VarStore
        regions = varStore.VarRegionList.Region

        # Find all the input locations; this finds "poles", that are
        # locations of the peaks, and "corners", that are locations
        # of the corners of the regions.  These two sets of locations
        # together constitute inputLocations to consider.

        poles = {(): None}  # Just using it as an ordered set
        inputLocations = set({()})
        for varData in varStore.VarData:
            regionIndices = varData.VarRegionIndex
            for regionIndex in regionIndices:
                peakLocation = []
                corners = []
                region = regions[regionIndex]
                for axisIndex, axis in enumerate(region.VarRegionAxis):
                    if axis.PeakCoord == 0:
                        continue
                    axisTag = axisTags[axisIndex]
                    peakLocation.append((axisTag, axis.PeakCoord))
                    corner = []
                    if axis.StartCoord != 0:
                        corner.append((axisTag, axis.StartCoord))
                    if axis.EndCoord != 0:
                        corner.append((axisTag, axis.EndCoord))
                    corners.append(corner)
                corners = set(product(*corners))
                peakLocation = tuple(peakLocation)
                poles[peakLocation] = None
                inputLocations.add(peakLocation)
                inputLocations.update(corners)

        # Sort them by number of axes, then by axis order
        inputLocations = [
            dict(t)
            for t in sorted(
                inputLocations,
                key=lambda t: (len(t), tuple(axisIndexes[tag] for tag, _ in t)),
            )
        ]
        poles = [dict(t) for t in poles.keys()]
        inputLocations = _pruneLocations(inputLocations, list(poles), axisTags)

        # Find the output locations, at input locations
        varIdxMap = avar.table.VarIdxMap
        instancer = VarStoreInstancer(varStore, fvarAxes)
        for location in inputLocations:
            instancer.setLocation(location)
            outputLocation = {}
            for axisIndex, axisTag in enumerate(axisTags):
                varIdx = axisIndex
                if varIdxMap is not None:
                    varIdx = varIdxMap[varIdx]
                delta = instancer[varIdx]
                if delta != 0:
                    v = location.get(axisTag, 0)
                    v = v + fi2fl(delta, 14)
                    # See https://github.com/fonttools/fonttools/pull/3598#issuecomment-2266082009
                    # v = max(-1, min(1, v))
                    outputLocation[axisTag] = v
            mappings.append((location, outputLocation))

        # Remove base master we added, if it maps to the default location
        assert mappings[0][0] == {}
        if mappings[0][1] == {}:
            mappings.pop(0)

    if denormalize:
        for tag, seg in axisMaps.items():
            if tag not in axisMap:
                raise ValueError(f"Unknown axis tag {tag}")
            denorm = lambda v: _denormalize(v, axisMap[tag])
            axisMaps[tag] = {denorm(k): denorm(v) for k, v in seg.items()}

        for i, (inputLoc, outputLoc) in enumerate(mappings):
            inputLoc = {
                tag: _denormalize(val, axisMap[tag]) for tag, val in inputLoc.items()
            }
            outputLoc = {
                tag: _denormalize(val, axisMap[tag]) for tag, val in outputLoc.items()
            }
            mappings[i] = (inputLoc, outputLoc)

    return axisMaps, mappings

