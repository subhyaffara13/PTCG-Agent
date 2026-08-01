
def getVFUserRegion(doc: DesignSpaceDocument, vf: VariableFontDescriptor) -> Region:
    vfUserRegion: Region = {}
    # For each axis, 2 cases:
    #  - it has a range = it's an axis in the VF DS
    #  - it's a single location = use it to know which rules should apply in the VF
    for axisSubset in vf.axisSubsets:
        axis = doc.getAxis(axisSubset.name)
        if axis is None:
            raise DesignSpaceDocumentError(
                f"Cannot find axis named '{axisSubset.name}' for variable font '{vf.name}'."
            )
        if hasattr(axisSubset, "userMinimum"):
            # Mypy doesn't support narrowing union types via hasattr()
            # TODO(Python 3.10): use TypeGuard
            # https://mypy.readthedocs.io/en/stable/type_narrowing.html
            axisSubset = cast(RangeAxisSubsetDescriptor, axisSubset)
            if not hasattr(axis, "minimum"):
                raise DesignSpaceDocumentError(
                    f"Cannot select a range over '{axis.name}' for variable font '{vf.name}' "
                    "because it's a discrete axis, use only 'userValue' instead."
                )
            axis = cast(AxisDescriptor, axis)
            vfUserRegion[axis.name] = Range(
                max(axisSubset.userMinimum, axis.minimum),
                min(axisSubset.userMaximum, axis.maximum),
                axisSubset.userDefault or axis.default,
            )
        else:
            axisSubset = cast(ValueAxisSubsetDescriptor, axisSubset)
            vfUserRegion[axis.name] = axisSubset.userValue
    # Any axis not mentioned explicitly has a single location = default value
    for axis in doc.axes:
        if axis.name not in vfUserRegion:
            assert isinstance(
                axis.default, (int, float)
            ), f"Axis '{axis.name}' has no valid default value."
            vfUserRegion[axis.name] = axis.default
    return vfUserRegion

