
def neuter_lookups(self, lookup_indices):
    """Sets lookups not in lookup_indices to None."""
    self.ensureDecompiled()
    self.Lookup = [
        l if i in lookup_indices else None for i, l in enumerate(self.Lookup)
    ]


def neuter_lookups(self, lookup_indices):
    """Sets lookups not in lookup_indices to None."""
    if self.table.LookupList:
        self.table.LookupList.neuter_lookups(lookup_indices)

