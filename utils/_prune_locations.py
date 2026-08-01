
def _pruneLocations(locations, poles, axisTags):
    # Now we have all the input locations, find which ones are
    # not needed and remove them.

    # Note: This algorithm is heavily tied to how VariationModel
    # is implemented.  It assumes that input was extracted from
    # VariationModel-generated object, like an ItemVariationStore
    # created by fontmake using varLib.models.VariationModel.
    # Some CoPilot blabbering:
    # I *think* I can prove that this algorithm is correct, but
    # I'm not 100% sure.  It's possible that there are edge cases
    # where this algorithm will fail.  I'm not sure how to prove
    # that it's correct, but I'm also not sure how to prove that
    # it's incorrect.  I'm not sure how to write a test case that
    # would prove that it's incorrect.  I'm not sure how to write
    # a test case that would prove that it's correct.

    model = VariationModel(locations, axisTags)
    modelMapping = model.mapping
    modelSupports = model.supports
    pins = {tuple(k.items()): None for k in poles}
    for location in poles:
        i = locations.index(location)
        i = modelMapping[i]
        support = modelSupports[i]
        supportAxes = set(support.keys())
        for axisTag, (minV, _, maxV) in support.items():
            for v in (minV, maxV):
                if v in (-1, 0, 1):
                    continue
                for pin in pins.keys():
                    pinLocation = dict(pin)
                    pinAxes = set(pinLocation.keys())
                    if pinAxes != supportAxes:
                        continue
                    if axisTag not in pinAxes:
                        continue
                    if pinLocation[axisTag] == v:
                        break
                else:
                    # No pin found. Go through the previous masters
                    # and find a suitable pin.  Going backwards is
                    # better because it can find a pin that is close
                    # to the pole in more dimensions, and reducing
                    # the total number of pins needed.
                    for candidateIdx in range(i - 1, -1, -1):
                        candidate = modelSupports[candidateIdx]
                        candidateAxes = set(candidate.keys())
                        if candidateAxes != supportAxes:
                            continue
                        if axisTag not in candidateAxes:
                            continue
                        candidate = {
                            k: defaultV for k, (_, defaultV, _) in candidate.items()
                        }
                        if candidate[axisTag] == v:
                            pins[tuple(candidate.items())] = None
                            break
                    else:
                        assert False, "No pin found"
    return [dict(t) for t in pins.keys()]

