
def load_designspace(designspace, log_enabled=True, *, require_sources=True):
    # TODO: remove this and always assume 'designspace' is a DesignSpaceDocument,
    # never a file path, as that's already handled by caller
    if hasattr(designspace, "sources"):  # Assume a DesignspaceDocument
        ds = designspace
    else:  # Assume a file path
        ds = DesignSpaceDocument.fromfile(designspace)

    masters = ds.sources
    if require_sources and not masters:
        raise VarLibValidationError("Designspace must have at least one source.")
    instances = ds.instances

    # TODO: Use fontTools.designspaceLib.tagForAxisName instead.
    standard_axis_map = OrderedDict(
        [
            ("weight", ("wght", {"en": "Weight"})),
            ("width", ("wdth", {"en": "Width"})),
            ("slant", ("slnt", {"en": "Slant"})),
            ("optical", ("opsz", {"en": "Optical Size"})),
            ("italic", ("ital", {"en": "Italic"})),
        ]
    )

    # Setup axes
    if not ds.axes:
        raise VarLibValidationError(f"Designspace must have at least one axis.")

    axes = OrderedDict()
    for axis_index, axis in enumerate(ds.axes):
        axis_name = axis.name
        if not axis_name:
            if not axis.tag:
                raise VarLibValidationError(f"Axis at index {axis_index} needs a tag.")
            axis_name = axis.name = axis.tag

        if axis_name in standard_axis_map:
            if axis.tag is None:
                axis.tag = standard_axis_map[axis_name][0]
            if not axis.labelNames:
                axis.labelNames.update(standard_axis_map[axis_name][1])
        else:
            if not axis.tag:
                raise VarLibValidationError(f"Axis at index {axis_index} needs a tag.")
            if not axis.labelNames:
                axis.labelNames["en"] = tostr(axis_name)

        axes[axis_name] = axis
    if log_enabled:
        log.info("Axes:\n%s", pformat([axis.asdict() for axis in axes.values()]))

    axisMappings = ds.axisMappings
    if axisMappings and log_enabled:
        log.info("Mappings:\n%s", pformat(axisMappings))

    # Check all master and instance locations are valid and fill in defaults
    for obj in masters + instances:
        obj_name = obj.name or obj.styleName or ""
        loc = obj.getFullDesignLocation(ds)
        obj.designLocation = loc
        if loc is None:
            raise VarLibValidationError(
                f"Source or instance '{obj_name}' has no location."
            )
        for axis_name in loc.keys():
            if axis_name not in axes:
                raise VarLibValidationError(
                    f"Location axis '{axis_name}' unknown for '{obj_name}'."
                )
        for axis_name, axis in axes.items():
            v = axis.map_backward(loc[axis_name])
            if not (axis.minimum <= v <= axis.maximum):
                raise VarLibValidationError(
                    f"Source or instance '{obj_name}' has out-of-range location "
                    f"for axis '{axis_name}': is mapped to {v} but must be in "
                    f"mapped range [{axis.minimum}..{axis.maximum}] (NOTE: all "
                    "values are in user-space)."
                )

    # Normalize master locations

    internal_master_locs = [o.getFullDesignLocation(ds) for o in masters]
    if log_enabled:
        log.info("Internal master locations:\n%s", pformat(internal_master_locs))

    # TODO This mapping should ideally be moved closer to logic in _add_fvar/avar
    internal_axis_supports = {}
    for axis in axes.values():
        triple = (axis.minimum, axis.default, axis.maximum)
        internal_axis_supports[axis.name] = [axis.map_forward(v) for v in triple]
    if log_enabled:
        log.info("Internal axis supports:\n%s", pformat(internal_axis_supports))

    normalized_master_locs = [
        models.normalizeLocation(m, internal_axis_supports)
        for m in internal_master_locs
    ]
    if log_enabled:
        log.info("Normalized master locations:\n%s", pformat(normalized_master_locs))

    # Find base master
    base_idx = None
    for i, m in enumerate(normalized_master_locs):
        if all(v == 0 for v in m.values()):
            if base_idx is not None:
                raise VarLibValidationError(
                    "More than one base master found in Designspace."
                )
            base_idx = i
    if require_sources and base_idx is None:
        raise VarLibValidationError(
            "Base master not found; no master at default location?"
        )
    if log_enabled:
        log.info("Index of base master: %s", base_idx)

    return _DesignSpaceData(
        axes,
        axisMappings,
        internal_axis_supports,
        base_idx,
        normalized_master_locs,
        masters,
        instances,
        ds.rules,
        ds.rulesProcessingLast,
        ds.lib,
    )

