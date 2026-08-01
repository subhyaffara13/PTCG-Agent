
def addFeatureVariationsRaw(font, table, conditionalSubstitutions, featureTag="rvrn"):
    """Low level implementation of addFeatureVariations that directly
    models the possibilities of the FeatureVariations table."""

    featureTags = [featureTag] if isinstance(featureTag, str) else sorted(featureTag)
    processLast = "rvrn" not in featureTags or len(featureTags) > 1

    #
    # if a <featureTag> feature is not present:
    #     make empty <featureTag> feature
    #     sort features, get <featureTag> feature index
    #     add <featureTag> feature to all scripts
    # if a <featureTag> feature is present:
    #     reuse <featureTag> feature index
    # make lookups
    # add feature variations
    #
    if table.Version < 0x00010001:
        table.Version = 0x00010001  # allow table.FeatureVariations

    varFeatureIndices = set()

    existingTags = {
        feature.FeatureTag
        for feature in table.FeatureList.FeatureRecord
        if feature.FeatureTag in featureTags
    }

    newTags = set(featureTags) - existingTags
    if newTags:
        varFeatures = []
        for featureTag in sorted(newTags):
            varFeature = buildFeatureRecord(featureTag, [])
            table.FeatureList.FeatureRecord.append(varFeature)
            varFeatures.append(varFeature)
        table.FeatureList.FeatureCount = len(table.FeatureList.FeatureRecord)

        sortFeatureList(table)

        for varFeature in varFeatures:
            varFeatureIndex = table.FeatureList.FeatureRecord.index(varFeature)

            for scriptRecord in table.ScriptList.ScriptRecord:
                if scriptRecord.Script.DefaultLangSys is None:
                    # We need to have a default LangSys to attach variations to.
                    langSys = ot.LangSys()
                    langSys.LookupOrder = None
                    langSys.ReqFeatureIndex = 0xFFFF
                    langSys.FeatureIndex = []
                    langSys.FeatureCount = 0
                    scriptRecord.Script.DefaultLangSys = langSys
                langSystems = [lsr.LangSys for lsr in scriptRecord.Script.LangSysRecord]
                for langSys in [scriptRecord.Script.DefaultLangSys] + langSystems:
                    langSys.FeatureIndex.append(varFeatureIndex)
                    langSys.FeatureCount = len(langSys.FeatureIndex)
            varFeatureIndices.add(varFeatureIndex)

    if existingTags:
        # indices may have changed if we inserted new features and sorted feature list
        # so we must do this after the above
        varFeatureIndices.update(
            index
            for index, feature in enumerate(table.FeatureList.FeatureRecord)
            if feature.FeatureTag in existingTags
        )

    axisIndices = {
        axis.axisTag: axisIndex for axisIndex, axis in enumerate(font["fvar"].axes)
    }

    hasFeatureVariations = (
        hasattr(table, "FeatureVariations") and table.FeatureVariations is not None
    )

    featureVariationRecords = []
    for conditionSet, lookupIndices in conditionalSubstitutions:
        conditionTable = []
        for axisTag, (minValue, maxValue) in sorted(conditionSet.items()):
            if minValue > maxValue:
                raise VarLibValidationError(
                    "A condition set has a minimum value above the maximum value."
                )
            ct = buildConditionTable(axisIndices[axisTag], minValue, maxValue)
            conditionTable.append(ct)
        records = []
        for varFeatureIndex in sorted(varFeatureIndices):
            existingLookupIndices = table.FeatureList.FeatureRecord[
                varFeatureIndex
            ].Feature.LookupListIndex
            combinedLookupIndices = (
                existingLookupIndices + lookupIndices
                if processLast
                else lookupIndices + existingLookupIndices
            )

            records.append(
                buildFeatureTableSubstitutionRecord(
                    varFeatureIndex, combinedLookupIndices
                )
            )
        if hasFeatureVariations and (
            fvr := findFeatureVariationRecord(table.FeatureVariations, conditionTable)
        ):
            fvr.FeatureTableSubstitution.SubstitutionRecord.extend(records)
            fvr.FeatureTableSubstitution.SubstitutionCount = len(
                fvr.FeatureTableSubstitution.SubstitutionRecord
            )
        else:
            featureVariationRecords.append(
                buildFeatureVariationRecord(conditionTable, records)
            )

    if hasFeatureVariations:
        if table.FeatureVariations.Version != 0x00010000:
            raise VarLibError(
                "Unsupported FeatureVariations table version: "
                f"0x{table.FeatureVariations.Version:08x} (expected 0x00010000)."
            )
        table.FeatureVariations.FeatureVariationRecord.extend(featureVariationRecords)
        table.FeatureVariations.FeatureVariationCount = len(
            table.FeatureVariations.FeatureVariationRecord
        )
    else:
        table.FeatureVariations = buildFeatureVariations(featureVariationRecords)

