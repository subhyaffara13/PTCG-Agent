
def buildFeatureTableSubstitutionRecord(featureIndex, lookupListIndices):
    """Build a FeatureTableSubstitutionRecord."""
    ftsr = ot.FeatureTableSubstitutionRecord()
    ftsr.FeatureIndex = featureIndex
    ftsr.Feature = ot.Feature()
    ftsr.Feature.LookupListIndex = lookupListIndices
    ftsr.Feature.LookupCount = len(lookupListIndices)
    return ftsr

