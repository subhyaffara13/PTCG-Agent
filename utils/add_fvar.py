
def addFvar(font, axes, instances):
    from .ttLib.tables._f_v_a_r import Axis, NamedInstance

    assert axes

    fvar = newTable("fvar")
    nameTable = font["name"]

    # if there are not currently any mac names don't add them here, that's inconsistent
    # https://github.com/fonttools/fonttools/issues/683
    macNames = any(nr.platformID == 1 for nr in getattr(nameTable, "names", ()))

    # we have all the best ways to express mac names
    platforms = ((3, 1, 0x409),)
    if macNames:
        platforms = ((1, 0, 0),) + platforms

    for axis_def in axes:
        axis = Axis()

        if isinstance(axis_def, tuple):
            (
                axis.axisTag,
                axis.minValue,
                axis.defaultValue,
                axis.maxValue,
                name,
            ) = axis_def
        else:
            (axis.axisTag, axis.minValue, axis.defaultValue, axis.maxValue, name) = (
                axis_def.tag,
                axis_def.minimum,
                axis_def.default,
                axis_def.maximum,
                axis_def.name,
            )
            if axis_def.hidden:
                axis.flags = 0x0001  # HIDDEN_AXIS

        if isinstance(name, str):
            name = dict(en=name)

        axis.axisNameID = nameTable.addMultilingualName(name, ttFont=font, mac=macNames)
        fvar.axes.append(axis)

    for instance in instances:
        if isinstance(instance, dict):
            coordinates = instance["location"]
            name = instance["stylename"]
            psname = instance.get("postscriptfontname")
        else:
            coordinates = instance.location
            name = instance.localisedStyleName or instance.styleName
            psname = instance.postScriptFontName

        if isinstance(name, str):
            name = dict(en=name)

        inst = NamedInstance()
        inst.subfamilyNameID = nameTable.addMultilingualName(
            name, ttFont=font, mac=macNames
        )
        if psname is not None:
            inst.postscriptNameID = nameTable.addName(psname, platforms=platforms)
        inst.coordinates = coordinates
        fvar.instances.append(inst)

    font["fvar"] = fvar

