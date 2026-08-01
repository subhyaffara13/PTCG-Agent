
def subset_lookups(self, lookup_indices):
    pass


def subset_lookups(self, lookup_indices):
    c = self.__subset_classify_context()

    if self.Format in [1, 2]:
        for rs in getattr(self, c.RuleSet):
            if not rs:
                continue
            for r in getattr(rs, c.Rule):
                if not r:
                    continue
                setattr(
                    r,
                    c.LookupRecord,
                    [
                        ll
                        for ll in getattr(r, c.LookupRecord)
                        if ll and ll.LookupListIndex in lookup_indices
                    ],
                )
                for ll in getattr(r, c.LookupRecord):
                    if not ll:
                        continue
                    ll.LookupListIndex = lookup_indices.index(ll.LookupListIndex)
    elif self.Format == 3:
        setattr(
            self,
            c.LookupRecord,
            [
                ll
                for ll in getattr(self, c.LookupRecord)
                if ll and ll.LookupListIndex in lookup_indices
            ],
        )
        for ll in getattr(self, c.LookupRecord):
            if not ll:
                continue
            ll.LookupListIndex = lookup_indices.index(ll.LookupListIndex)
    else:
        assert 0, "unknown format: %s" % self.Format


def subset_lookups(self, lookup_indices):
    if self.Format == 1:
        return self.ExtSubTable.subset_lookups(lookup_indices)
    else:
        assert 0, "unknown format: %s" % self.Format


def subset_lookups(self, lookup_indices):
    for s in self.SubTable:
        s.subset_lookups(lookup_indices)


def subset_lookups(self, lookup_indices):
    self.ensureDecompiled()
    self.Lookup = [self.Lookup[i] for i in lookup_indices if i < self.LookupCount]
    self.LookupCount = len(self.Lookup)
    for l in self.Lookup:
        l.subset_lookups(lookup_indices)


def subset_lookups(self, lookup_indices):
    """ "Returns True if feature is non-empty afterwards."""
    self.LookupListIndex = [l for l in self.LookupListIndex if l in lookup_indices]
    # Now map them.
    self.LookupListIndex = [lookup_indices.index(l) for l in self.LookupListIndex]
    self.LookupCount = len(self.LookupListIndex)
    # keep 'size' feature even if it contains no lookups; but drop any other
    # empty feature (e.g. FeatureParams for stylistic set names)
    # https://github.com/fonttools/fonttools/issues/2324
    return self.LookupCount or isinstance(
        self.FeatureParams, otTables.FeatureParamsSize
    )


def subset_lookups(self, lookup_indices):
    """Returns the indices of nonempty features."""
    # Note: Never ever drop feature 'pref', even if it's empty.
    # HarfBuzz chooses shaper for Khmer based on presence of this
    # feature.	See thread at:
    # http://lists.freedesktop.org/archives/harfbuzz/2012-November/002660.html
    return [
        i
        for i, f in enumerate(self.FeatureRecord)
        if (f.Feature.subset_lookups(lookup_indices) or f.FeatureTag == "pref")
    ]


def subset_lookups(self, lookup_indices):
    """Returns the indices of nonempty features."""
    return [
        r.FeatureIndex
        for r in self.SubstitutionRecord
        if r.Feature.subset_lookups(lookup_indices)
    ]


def subset_lookups(self, lookup_indices):
    """Returns the indices of nonempty features."""
    return sum(
        (
            f.FeatureTableSubstitution.subset_lookups(lookup_indices)
            for f in self.FeatureVariationRecord
        ),
        [],
    )


def subset_lookups(self, lookup_indices):
    """Retains specified lookups, then removes empty features, language
    systems, and scripts."""
    if self.table.LookupList:
        self.table.LookupList.subset_lookups(lookup_indices)
    if self.table.FeatureList:
        feature_indices = self.table.FeatureList.subset_lookups(lookup_indices)
    else:
        feature_indices = []
    if getattr(self.table, "FeatureVariations", None):
        feature_indices += self.table.FeatureVariations.subset_lookups(lookup_indices)
    feature_indices = _uniq_sort(feature_indices)
    if self.table.FeatureList:
        self.table.FeatureList.subset_features(feature_indices)
    if getattr(self.table, "FeatureVariations", None):
        self.table.FeatureVariations.subset_features(feature_indices)
    if self.table.ScriptList:
        self.table.ScriptList.subset_features(
            feature_indices, self.retain_empty_scripts()
        )

