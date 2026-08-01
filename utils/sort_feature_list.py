
def sortFeatureList(table):
    """Sort the feature list by feature tag, and remap the feature indices
    elsewhere. This is needed after the feature list has been modified.
    """
    # decorate, sort, undecorate, because we need to make an index remapping table
    tagIndexFea = [
        (fea.FeatureTag, index, fea)
        for index, fea in enumerate(table.FeatureList.FeatureRecord)
    ]
    tagIndexFea.sort()
    table.FeatureList.FeatureRecord = [fea for tag, index, fea in tagIndexFea]
    featureRemap = dict(
        zip([index for tag, index, fea in tagIndexFea], range(len(tagIndexFea)))
    )

    # Remap the feature indices
    remapFeatures(table, featureRemap)

