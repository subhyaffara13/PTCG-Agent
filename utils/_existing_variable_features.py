
def _existingVariableFeatures(table):
    existingFeatureVarsTags = set()
    if hasattr(table, "FeatureVariations") and table.FeatureVariations is not None:
        features = table.FeatureList.FeatureRecord
        for fvr in table.FeatureVariations.FeatureVariationRecord:
            for ftsr in fvr.FeatureTableSubstitution.SubstitutionRecord:
                existingFeatureVarsTags.add(features[ftsr.FeatureIndex].FeatureTag)
    return existingFeatureVarsTags

