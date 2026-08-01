
def subset_features(self, feature_indices):
    self.ensureDecompiled()
    self.FeatureRecord = _list_subset(self.FeatureRecord, feature_indices)
    self.FeatureCount = len(self.FeatureRecord)
    return bool(self.FeatureCount)


def subset_features(self, feature_indices):
    self.ensureDecompiled()
    self.SubstitutionRecord = [
        r for r in self.SubstitutionRecord if r.FeatureIndex in feature_indices
    ]
    # remap feature indices
    for r in self.SubstitutionRecord:
        r.FeatureIndex = feature_indices.index(r.FeatureIndex)
    self.SubstitutionCount = len(self.SubstitutionRecord)
    return bool(self.SubstitutionCount)


def subset_features(self, feature_indices):
    self.ensureDecompiled()
    for r in self.FeatureVariationRecord:
        r.FeatureTableSubstitution.subset_features(feature_indices)
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


def subset_features(self, feature_indices):
    if self.ReqFeatureIndex in feature_indices:
        self.ReqFeatureIndex = feature_indices.index(self.ReqFeatureIndex)
    else:
        self.ReqFeatureIndex = 65535
    self.FeatureIndex = [f for f in self.FeatureIndex if f in feature_indices]
    # Now map them.
    self.FeatureIndex = [
        feature_indices.index(f) for f in self.FeatureIndex if f in feature_indices
    ]
    self.FeatureCount = len(self.FeatureIndex)
    return bool(self.FeatureCount or self.ReqFeatureIndex != 65535)


def subset_features(self, feature_indices, keepEmptyDefaultLangSys=False):
    if (
        self.DefaultLangSys
        and not self.DefaultLangSys.subset_features(feature_indices)
        and not keepEmptyDefaultLangSys
    ):
        self.DefaultLangSys = None
    self.LangSysRecord = [
        l for l in self.LangSysRecord if l.LangSys.subset_features(feature_indices)
    ]
    self.LangSysCount = len(self.LangSysRecord)
    return bool(self.LangSysCount or self.DefaultLangSys)


def subset_features(self, feature_indices, retain_empty):
    # https://bugzilla.mozilla.org/show_bug.cgi?id=1331737#c32
    self.ScriptRecord = [
        s
        for s in self.ScriptRecord
        if s.Script.subset_features(feature_indices, s.ScriptTag == "DFLT")
        or retain_empty
    ]
    self.ScriptCount = len(self.ScriptRecord)
    return bool(self.ScriptCount)

