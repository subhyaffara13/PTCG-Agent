
def buildFeatureVariations(featureVariationRecords):
    """Build the FeatureVariations subtable."""
    fv = ot.FeatureVariations()
    fv.Version = 0x00010000
    fv.FeatureVariationRecord = featureVariationRecords
    fv.FeatureVariationCount = len(featureVariationRecords)
    return fv

