
def findFeatureVariationRecord(featureVariations, conditionTable):
    """Find a FeatureVariationRecord that has the same conditionTable."""
    if featureVariations.Version != 0x00010000:
        raise VarLibError(
            "Unsupported FeatureVariations table version: "
            f"0x{featureVariations.Version:08x} (expected 0x00010000)."
        )

    for fvr in featureVariations.FeatureVariationRecord:
        if conditionTable == fvr.ConditionSet.ConditionTable:
            return fvr

    return None

