
def _add_avar(font, axes, mappings, axisTags):
    """
    Add 'avar' table to font.

    axes is an ordered dictionary of AxisDescriptor objects.
    """

    assert axes
    assert isinstance(axes, OrderedDict)

    log.info("Generating avar")

    avar = newTable("avar")

    interesting = False
    vals_triples = {}
    for axis in axes.values():
        # Currently, some rasterizers require that the default value maps
        # (-1 to -1, 0 to 0, and 1 to 1) be present for all the segment
        # maps, even when the default normalization mapping for the axis
        # was not modified.
        # https://github.com/googlei18n/fontmake/issues/295
        # https://github.com/fonttools/fonttools/issues/1011
        # TODO(anthrotype) revert this (and 19c4b37) when issue is fixed
        curve = avar.segments[axis.tag] = {-1.0: -1.0, 0.0: 0.0, 1.0: 1.0}

        keys_triple = (axis.minimum, axis.default, axis.maximum)
        vals_triple = tuple(axis.map_forward(v) for v in keys_triple)
        vals_triples[axis.tag] = vals_triple

        if not axis.map:
            continue

        items = sorted(axis.map)
        keys = [item[0] for item in items]
        vals = [item[1] for item in items]

        # Current avar requirements.  We don't have to enforce
        # these on the designer and can deduce some ourselves,
        # but for now just enforce them.
        if axis.minimum != min(keys):
            raise VarLibValidationError(
                f"Axis '{axis.name}': there must be a mapping for the axis minimum "
                f"value {axis.minimum} and it must be the lowest input mapping value."
            )
        if axis.maximum != max(keys):
            raise VarLibValidationError(
                f"Axis '{axis.name}': there must be a mapping for the axis maximum "
                f"value {axis.maximum} and it must be the highest input mapping value."
            )
        if axis.default not in keys:
            raise VarLibValidationError(
                f"Axis '{axis.name}': there must be a mapping for the axis default "
                f"value {axis.default}."
            )
        # No duplicate input values (output values can be >= their preceeding value).
        if len(set(keys)) != len(keys):
            raise VarLibValidationError(
                f"Axis '{axis.name}': All axis mapping input='...' values must be "
                "unique, but we found duplicates."
            )
        # Ascending values
        if sorted(vals) != vals:
            raise VarLibValidationError(
                f"Axis '{axis.name}': mapping output values must be in ascending order."
            )

        keys = [models.normalizeValue(v, keys_triple) for v in keys]
        vals = [models.normalizeValue(v, vals_triple) for v in vals]

        if all(k == v for k, v in zip(keys, vals)):
            continue
        interesting = True

        curve.update(zip(keys, vals))

        assert 0.0 in curve and curve[0.0] == 0.0
        assert -1.0 not in curve or curve[-1.0] == -1.0
        assert +1.0 not in curve or curve[+1.0] == +1.0
        # curve.update({-1.0: -1.0, 0.0: 0.0, 1.0: 1.0})

    if mappings:
        interesting = True

        inputLocations = [
            {
                axes[name].tag: models.normalizeValue(v, vals_triples[axes[name].tag])
                for name, v in mapping.inputLocation.items()
            }
            for mapping in mappings
        ]
        outputLocations = [
            {
                axes[name].tag: models.normalizeValue(v, vals_triples[axes[name].tag])
                for name, v in mapping.outputLocation.items()
            }
            for mapping in mappings
        ]
        assert len(inputLocations) == len(outputLocations)

        # If base-master is missing, insert it at zero location.
        if not any(all(v == 0 for k, v in loc.items()) for loc in inputLocations):
            inputLocations.insert(0, {})
            outputLocations.insert(0, {})

        model = models.VariationModel(inputLocations, axisTags)
        storeBuilder = varStore.OnlineVarStoreBuilder(axisTags)
        storeBuilder.setModel(model)
        varIdxes = {}
        for tag in axisTags:
            masterValues = []
            for vo, vi in zip(outputLocations, inputLocations):
                if tag not in vo:
                    masterValues.append(0)
                    continue
                v = vo[tag] - vi.get(tag, 0)
                masterValues.append(fl2fi(v, 14))
            varIdxes[tag] = storeBuilder.storeMasters(masterValues)[1]

        store = storeBuilder.finish()
        optimized = store.optimize()
        varIdxes = {axis: optimized[value] for axis, value in varIdxes.items()}

        varIdxMap = builder.buildDeltaSetIndexMap(varIdxes[t] for t in axisTags)

        avar.majorVersion = 2
        avar.table = ot.avar()
        avar.table.VarIdxMap = varIdxMap
        avar.table.VarStore = store

    assert "avar" not in font
    if not interesting:
        log.info("No need for avar")
        avar = None
    else:
        font["avar"] = avar

    return avar

