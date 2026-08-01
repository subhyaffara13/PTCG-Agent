
def buildFeatureRecord(featureTag, lookupListIndices):
    """Build a FeatureRecord."""
    fr = ot.FeatureRecord()
    fr.FeatureTag = featureTag
    fr.Feature = ot.Feature()
    fr.Feature.LookupListIndex = lookupListIndices
    fr.Feature.populateDefaults()
    return fr

