
def collect_lookups(self):
    return []


def collect_lookups(self):
    c = self.__subset_classify_context()

    if self.Format in [1, 2]:
        return [
            ll.LookupListIndex
            for rs in getattr(self, c.RuleSet)
            if rs
            for r in getattr(rs, c.Rule)
            if r
            for ll in getattr(r, c.LookupRecord)
            if ll
        ]
    elif self.Format == 3:
        return [ll.LookupListIndex for ll in getattr(self, c.LookupRecord) if ll]
    else:
        assert 0, "unknown format: %s" % self.Format


def collect_lookups(self):
    if self.Format == 1:
        return self.ExtSubTable.collect_lookups()
    else:
        assert 0, "unknown format: %s" % self.Format


def collect_lookups(self):
    return sum((st.collect_lookups() for st in self.SubTable if st), [])


def collect_lookups(self, feature_indices):
    return sum(
        (
            self.FeatureRecord[i].Feature.LookupListIndex
            for i in feature_indices
            if i < self.FeatureCount
        ),
        [],
    )


def collect_lookups(self, feature_indices):
    return sum(
        (
            r.Feature.LookupListIndex
            for vr in self.FeatureVariationRecord
            for r in vr.FeatureTableSubstitution.SubstitutionRecord
            if r.FeatureIndex in feature_indices
        ),
        [],
    )

