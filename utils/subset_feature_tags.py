
def subset_feature_tags(self, feature_tags):
    if self.table.FeatureList:
        feature_indices = [
            i
            for i, f in enumerate(self.table.FeatureList.FeatureRecord)
            if f.FeatureTag in feature_tags
        ]
        self.table.FeatureList.subset_features(feature_indices)
        if getattr(self.table, "FeatureVariations", None):
            self.table.FeatureVariations.subset_features(feature_indices)
    else:
        feature_indices = []
    if self.table.ScriptList:
        self.table.ScriptList.subset_features(
            feature_indices, self.retain_empty_scripts()
        )

