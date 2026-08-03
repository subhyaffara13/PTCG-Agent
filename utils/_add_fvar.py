from typing import List

def _add_fvar(font, axes, instances: List[InstanceDescriptor]):
    """
    Add 'fvar' table to font.

    axes is an ordered dictionary of DesignspaceAxis objects.

    instances is list of dictionary objects with 'location', 'stylename',
    and possibly 'postscriptfontname' entries.
    """

    assert axes
    assert isinstance(axes, OrderedDict)

    log.info("Generating fvar")

    fvar = newTable("fvar")
    nameTable = font["name"]

    # if there are not currently any mac names don't add them here, that's inconsistent
    # https://github.com/fonttools/fonttools/issues/683
    macNames = any(nr.platformID == 1 for nr in getattr(nameTable, "names", ()))

    # we have all the best ways to express mac names
    platforms = ((3, 1, 0x409),)
    if macNames:
        platforms = ((1, 0, 0),) + platforms

    for a in axes.values():
        axis = Axis()
        axis.axisTag = Tag(a.tag)
        # TODO Skip axes that have no variation.
        axis.minValue, axis.defaultValue, axis.maxValue = (
            a.minimum,
            a.default,
            a.maximum,
        )
        axis.axisNameID = nameTable.addMultilingualName(
            a.labelNames, font, minNameID=256, mac=macNames
        )
        axis.flags = int(a.hidden)
        fvar.axes.append(axis)

    default_coordinates = {axis.axisTag: axis.defaultValue for axis in fvar.axes}

    for instance in instances:
        # Filter out discrete axis locations
        coordinates = {
            name: value for name, value in instance.location.items() if name in axes
        }

        if "en" not in instance.localisedStyleName:
            if not instance.styleName:
                raise VarLibValidationError(
                    f"Instance at location '{coordinates}' must have a default English "
                    "style name ('stylename' attribute on the instance element or a "
                    "stylename element with an 'xml:lang=\"en\"' attribute)."
                )
            localisedStyleName = dict(instance.localisedStyleName)
            localisedStyleName["en"] = tostr(instance.styleName)
        else:
            localisedStyleName = instance.localisedStyleName

        psname = instance.postScriptFontName

        inst = NamedInstance()
        inst.coordinates = {
            axes[k].tag: axes[k].map_backward(v) for k, v in coordinates.items()
        }

        subfamilyNameID = nameTable.findMultilingualName(
            localisedStyleName, windows=True, mac=macNames
        )
        if subfamilyNameID in {2, 17} and inst.coordinates == default_coordinates:
            # Instances can only reuse an existing name ID 2 or 17 if they are at the
            # default location across all axes, see:
            # https://github.com/fonttools/fonttools/issues/3825.
            inst.subfamilyNameID = subfamilyNameID
        else:
            inst.subfamilyNameID = nameTable.addMultilingualName(
                localisedStyleName, windows=True, mac=macNames, minNameID=256
            )

        if psname is not None:
            psname = tostr(psname)
            inst.postscriptNameID = nameTable.addName(psname, platforms=platforms)
        fvar.instances.append(inst)

    assert "fvar" not in font
    font["fvar"] = fvar

    return fvar

