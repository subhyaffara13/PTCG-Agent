
def prune_features(self, feature_index_map):
    self.ensureDecompiled()
    self.SubstitutionRecord = [
        r for r in self.SubstitutionRecord if r.FeatureIndex in feature_index_map.keys()
    ]
    # remap feature indices
    for r in self.SubstitutionRecord:
        r.FeatureIndex = feature_index_map[r.FeatureIndex]
    self.SubstitutionCount = len(self.SubstitutionRecord)
    return bool(self.SubstitutionCount)


def prune_features(self, feature_index_map):
    self.ensureDecompiled()
    for r in self.FeatureVariationRecord:
        r.FeatureTableSubstitution.prune_features(feature_index_map)
    # Prune empty records at the end only
    # https://github.com/fonttools/fonttools/issues/1881
    while (
        self.FeatureVariationRecord
        and not self.FeatureVariationRecord[
            -1
        ].FeatureTableSubstitution.SubstitutionCount
    ):
        self.FeatureVariationRecord.pop()
    self.FeatureVariationCount = len(self.FeatureVariationRecord)
    return bool(self.FeatureVariationCount)


def prune_features(self, feature_index_map):
    self.ReqFeatureIndex = feature_index_map.get(self.ReqFeatureIndex, 65535)
    self.FeatureIndex = [
        feature_index_map[f] for f in self.FeatureIndex if f in feature_index_map.keys()
    ]
    self.FeatureCount = len(self.FeatureIndex)
    return bool(self.FeatureCount or self.ReqFeatureIndex != 65535)


def prune_features(self, feature_index_map, keepEmptyDefaultLangSys=False):
    if (
        self.DefaultLangSys
        and not self.DefaultLangSys.prune_features(feature_index_map)
        and not keepEmptyDefaultLangSys
    ):
        self.DefaultLangSys = None
    self.LangSysRecord = [
        l for l in self.LangSysRecord if l.LangSys.prune_features(feature_index_map)
    ]
    self.LangSysCount = len(self.LangSysRecord)
    return bool(self.LangSysCount or self.DefaultLangSys)


def prune_features(self, feature_index_map, retain_empty):
    # https://bugzilla.mozilla.org/show_bug.cgi?id=1331737#c32
    self.ScriptRecord = [
        s
        for s in self.ScriptRecord
        if s.Script.prune_features(feature_index_map, s.ScriptTag == "DFLT")
        or retain_empty
    ]
    self.ScriptCount = len(self.ScriptRecord)
    return bool(self.ScriptCount)


def prune_features(self):
    """Remove unreferenced and duplicate features in FeatureList
    Remove unreferenced features and remap duplicate feature indices in ScriptList and FeatureVariations
    """
    if self.table.ScriptList:
        feature_indices = self.table.ScriptList.collect_features()
    else:
        feature_indices = []
    (feature_indices, feature_index_map) = self.remap_duplicate_features(
        feature_indices
    )

    if self.table.FeatureList:
        self.table.FeatureList.subset_features(feature_indices)
    if getattr(self.table, "FeatureVariations", None):
        self.table.FeatureVariations.prune_features(feature_index_map)
    if self.table.ScriptList:
        self.table.ScriptList.prune_features(
            feature_index_map, self.retain_empty_scripts()
        )

