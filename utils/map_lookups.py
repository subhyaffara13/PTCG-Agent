
def mapLookups(self, lookupMap):
    pass


def mapLookups(self, lookupMap):
    c = self.__merge_classify_context()

    if self.Format in [1, 2]:
        for rs in getattr(self, c.RuleSet):
            if not rs:
                continue
            for r in getattr(rs, c.Rule):
                if not r:
                    continue
                for ll in getattr(r, c.LookupRecord):
                    if not ll:
                        continue
                    ll.LookupListIndex = lookupMap[ll.LookupListIndex]
    elif self.Format == 3:
        for ll in getattr(self, c.LookupRecord):
            if not ll:
                continue
            ll.LookupListIndex = lookupMap[ll.LookupListIndex]
    else:
        assert 0, "unknown format: %s" % self.Format


def mapLookups(self, lookupMap):
    if self.Format == 1:
        self.ExtSubTable.mapLookups(lookupMap)
    else:
        assert 0, "unknown format: %s" % self.Format


def mapLookups(self, lookupMap):
    for st in self.SubTable:
        if not st:
            continue
        st.mapLookups(lookupMap)


def mapLookups(self, lookupMap):
    for l in self.Lookup:
        if not l:
            continue
        l.mapLookups(lookupMap)


def mapLookups(self, lookupMap):
    self.LookupListIndex = [lookupMap[i] for i in self.LookupListIndex]


def mapLookups(self, lookupMap):
    for f in self.FeatureRecord:
        if not f or not f.Feature:
            continue
        f.Feature.mapLookups(lookupMap)

