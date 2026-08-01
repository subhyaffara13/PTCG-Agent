
def _extractSubSpace(
    doc: DesignSpaceDocument,
    userRegion: Region,
    *,
    keepVFs: bool,
    makeNames: bool,
    expandLocations: bool,
    makeInstanceFilename: MakeInstanceFilenameCallable,
) -> DesignSpaceDocument:
    subDoc = DesignSpaceDocument()
    # Don't include STAT info
    # FIXME: (Jany) let's think about it. Not include = OK because the point of
    # the splitting is to build VFs and we'll use the STAT data of the full
    # document to generate the STAT of the VFs, so "no need" to have STAT data
    # in sub-docs. Counterpoint: what if someone wants to split this DS for
    # other purposes?  Maybe for that it would be useful to also subset the STAT
    # data?
    # subDoc.elidedFallbackName = doc.elidedFallbackName

    def maybeExpandDesignLocation(object):
        if expandLocations:
            return object.getFullDesignLocation(doc)
        else:
            return object.designLocation

    for axis in doc.axes:
        range = userRegion[axis.name]
        if isinstance(range, Range) and hasattr(axis, "minimum"):
            # Mypy doesn't support narrowing union types via hasattr()
            # TODO(Python 3.10): use TypeGuard
            # https://mypy.readthedocs.io/en/stable/type_narrowing.html
            axis = cast(AxisDescriptor, axis)
            subDoc.addAxis(
                AxisDescriptor(
                    # Same info
                    tag=axis.tag,
                    name=axis.name,
                    labelNames=axis.labelNames,
                    hidden=axis.hidden,
                    # Subset range
                    minimum=max(range.minimum, axis.minimum),
                    default=range.default or axis.default,
                    maximum=min(range.maximum, axis.maximum),
                    map=[
                        (user, design)
                        for user, design in axis.map
                        if range.minimum <= user <= range.maximum
                    ],
                    # Don't include STAT info
                    axisOrdering=None,
                    axisLabels=None,
                )
            )

    subDoc.axisMappings = mappings = []
    subDocAxes = {axis.name for axis in subDoc.axes}
    for mapping in doc.axisMappings:
        if not all(axis in subDocAxes for axis in mapping.inputLocation.keys()):
            continue
        if not all(axis in subDocAxes for axis in mapping.outputLocation.keys()):
            LOGGER.error(
                "In axis mapping from input %s, some output axes are not in the variable-font: %s",
                mapping.inputLocation,
                mapping.outputLocation,
            )
            continue

        mappingAxes = set()
        mappingAxes.update(mapping.inputLocation.keys())
        mappingAxes.update(mapping.outputLocation.keys())
        for axis in doc.axes:
            if axis.name not in mappingAxes:
                continue
            range = userRegion[axis.name]
            if (
                range.minimum != axis.minimum
                or (range.default is not None and range.default != axis.default)
                or range.maximum != axis.maximum
            ):
                LOGGER.error(
                    "Limiting axis ranges used in <mapping> elements not supported: %s",
                    axis.name,
                )
                continue

        mappings.append(
            AxisMappingDescriptor(
                inputLocation=mapping.inputLocation,
                outputLocation=mapping.outputLocation,
            )
        )

    # Don't include STAT info
    # subDoc.locationLabels = doc.locationLabels

    # Rules: subset them based on conditions
    designRegion = userRegionToDesignRegion(doc, userRegion)
    subDoc.rules = _subsetRulesBasedOnConditions(doc.rules, designRegion)
    subDoc.rulesProcessingLast = doc.rulesProcessingLast

    # Sources: keep only the ones that fall within the kept axis ranges
    for source in doc.sources:
        if not locationInRegion(doc.map_backward(source.designLocation), userRegion):
            continue

        subDoc.addSource(
            SourceDescriptor(
                filename=source.filename,
                path=source.path,
                font=source.font,
                name=source.name,
                designLocation=_filterLocation(
                    userRegion, maybeExpandDesignLocation(source)
                ),
                layerName=source.layerName,
                familyName=source.familyName,
                styleName=source.styleName,
                muteKerning=source.muteKerning,
                muteInfo=source.muteInfo,
                mutedGlyphNames=source.mutedGlyphNames,
            )
        )

    # Copy family name translations from the old default source to the new default
    vfDefault = subDoc.findDefault()
    oldDefault = doc.findDefault()
    if vfDefault is not None and oldDefault is not None:
        vfDefault.localisedFamilyName = oldDefault.localisedFamilyName

    # Variable fonts: keep only the ones that fall within the kept axis ranges
    if keepVFs:
        # Note: call getVariableFont() to make the implicit VFs explicit
        for vf in doc.getVariableFonts():
            vfUserRegion = getVFUserRegion(doc, vf)
            if regionInRegion(vfUserRegion, userRegion):
                subDoc.addVariableFont(
                    VariableFontDescriptor(
                        name=vf.name,
                        filename=vf.filename,
                        axisSubsets=[
                            axisSubset
                            for axisSubset in vf.axisSubsets
                            if isinstance(userRegion[axisSubset.name], Range)
                        ],
                        lib=vf.lib,
                    )
                )

    # Instances: same as Sources + compute missing names
    for instance in doc.instances:
        if not locationInRegion(instance.getFullUserLocation(doc), userRegion):
            continue

        if makeNames:
            statNames = getStatNames(doc, instance.getFullUserLocation(doc))
            familyName = instance.familyName or statNames.familyNames.get("en")
            styleName = instance.styleName or statNames.styleNames.get("en")
            subDoc.addInstance(
                InstanceDescriptor(
                    filename=instance.filename
                    or makeInstanceFilename(doc, instance, statNames),
                    path=instance.path,
                    font=instance.font,
                    name=instance.name or f"{familyName} {styleName}",
                    userLocation={} if expandLocations else instance.userLocation,
                    designLocation=_filterLocation(
                        userRegion, maybeExpandDesignLocation(instance)
                    ),
                    familyName=familyName,
                    styleName=styleName,
                    postScriptFontName=instance.postScriptFontName
                    or statNames.postScriptFontName,
                    styleMapFamilyName=instance.styleMapFamilyName
                    or statNames.styleMapFamilyNames.get("en"),
                    styleMapStyleName=instance.styleMapStyleName
                    or statNames.styleMapStyleName,
                    localisedFamilyName=instance.localisedFamilyName
                    or statNames.familyNames,
                    localisedStyleName=instance.localisedStyleName
                    or statNames.styleNames,
                    localisedStyleMapFamilyName=instance.localisedStyleMapFamilyName
                    or statNames.styleMapFamilyNames,
                    localisedStyleMapStyleName=instance.localisedStyleMapStyleName
                    or {},
                    lib=instance.lib,
                )
            )
        else:
            subDoc.addInstance(
                InstanceDescriptor(
                    filename=instance.filename,
                    path=instance.path,
                    font=instance.font,
                    name=instance.name,
                    userLocation={} if expandLocations else instance.userLocation,
                    designLocation=_filterLocation(
                        userRegion, maybeExpandDesignLocation(instance)
                    ),
                    familyName=instance.familyName,
                    styleName=instance.styleName,
                    postScriptFontName=instance.postScriptFontName,
                    styleMapFamilyName=instance.styleMapFamilyName,
                    styleMapStyleName=instance.styleMapStyleName,
                    localisedFamilyName=instance.localisedFamilyName,
                    localisedStyleName=instance.localisedStyleName,
                    localisedStyleMapFamilyName=instance.localisedStyleMapFamilyName,
                    localisedStyleMapStyleName=instance.localisedStyleMapStyleName,
                    lib=instance.lib,
                )
            )

    subDoc.lib = doc.lib

    return subDoc

