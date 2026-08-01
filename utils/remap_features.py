
def remapFeatures(table, featureRemap):
    """Go through the scripts list, and remap feature indices."""
    for scriptIndex, script in enumerate(table.ScriptList.ScriptRecord):
        defaultLangSys = script.Script.DefaultLangSys
        if defaultLangSys is not None:
            _remapLangSys(defaultLangSys, featureRemap)
        for langSysRecordIndex, langSysRec in enumerate(script.Script.LangSysRecord):
            langSys = langSysRec.LangSys
            _remapLangSys(langSys, featureRemap)

    if hasattr(table, "FeatureVariations") and table.FeatureVariations is not None:
        for fvr in table.FeatureVariations.FeatureVariationRecord:
            for ftsr in fvr.FeatureTableSubstitution.SubstitutionRecord:
                ftsr.FeatureIndex = featureRemap[ftsr.FeatureIndex]

