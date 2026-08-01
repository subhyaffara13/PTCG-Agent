
def mapMarkFilteringSets(self, markFilteringSetMap):
    if self.LookupFlag & 0x0010:
        self.MarkFilteringSet = markFilteringSetMap[self.MarkFilteringSet]


def mapMarkFilteringSets(self, markFilteringSetMap):
    for l in self.Lookup:
        if not l:
            continue
        l.mapMarkFilteringSets(markFilteringSetMap)

