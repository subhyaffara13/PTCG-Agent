
def buildFeatureVariationRecord(conditionTable, substitutionRecords):
    """Build a FeatureVariationRecord."""
    fvr = ot.FeatureVariationRecord()
    if len(conditionTable) != 0:
        fvr.ConditionSet = ot.ConditionSet()
        fvr.ConditionSet.ConditionTable = conditionTable
        fvr.ConditionSet.ConditionCount = len(conditionTable)
    else:
        fvr.ConditionSet = None
    fvr.FeatureTableSubstitution = ot.FeatureTableSubstitution()
    fvr.FeatureTableSubstitution.Version = 0x00010000
    fvr.FeatureTableSubstitution.SubstitutionRecord = substitutionRecords
    fvr.FeatureTableSubstitution.SubstitutionCount = len(substitutionRecords)
    return fvr

