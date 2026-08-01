
def layoutPostMerge(font):
    # Map references back to indices

    GDEF = font.get("GDEF")
    GSUB = font.get("GSUB")
    GPOS = font.get("GPOS")

    for t in [GSUB, GPOS]:
        if not t:
            continue

        if t.table.FeatureList and t.table.ScriptList:
            # Collect unregistered (new) features.
            featureMap = GregariousIdentityDict(t.table.FeatureList.FeatureRecord)
            t.table.ScriptList.mapFeatures(featureMap)

            # Record used features.
            featureMap = AttendanceRecordingIdentityDict(
                t.table.FeatureList.FeatureRecord
            )
            t.table.ScriptList.mapFeatures(featureMap)
            usedIndices = featureMap.s

            # Remove unused features
            t.table.FeatureList.FeatureRecord = [
                f
                for i, f in enumerate(t.table.FeatureList.FeatureRecord)
                if i in usedIndices
            ]

            # Map back to indices.
            featureMap = NonhashableDict(t.table.FeatureList.FeatureRecord)
            t.table.ScriptList.mapFeatures(featureMap)

            t.table.FeatureList.FeatureCount = len(t.table.FeatureList.FeatureRecord)

        if t.table.LookupList:
            # Collect unregistered (new) lookups.
            lookupMap = GregariousIdentityDict(t.table.LookupList.Lookup)
            t.table.FeatureList.mapLookups(lookupMap)
            t.table.LookupList.mapLookups(lookupMap)

            # Record used lookups.
            lookupMap = AttendanceRecordingIdentityDict(t.table.LookupList.Lookup)
            t.table.FeatureList.mapLookups(lookupMap)
            t.table.LookupList.mapLookups(lookupMap)
            usedIndices = lookupMap.s

            # Remove unused lookups
            t.table.LookupList.Lookup = [
                l for i, l in enumerate(t.table.LookupList.Lookup) if i in usedIndices
            ]

            # Map back to indices.
            lookupMap = NonhashableDict(t.table.LookupList.Lookup)
            t.table.FeatureList.mapLookups(lookupMap)
            t.table.LookupList.mapLookups(lookupMap)

            t.table.LookupList.LookupCount = len(t.table.LookupList.Lookup)

            if GDEF and GDEF.table.Version >= 0x00010002:
                markFilteringSetMap = NonhashableDict(
                    GDEF.table.MarkGlyphSetsDef.Coverage
                )
                t.table.LookupList.mapMarkFilteringSets(markFilteringSetMap)

