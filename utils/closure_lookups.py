
def closure_lookups(self, lookup_indices):
    """Returns sorted index of all lookups reachable from lookup_indices."""
    lookup_indices = _uniq_sort(lookup_indices)
    recurse = lookup_indices
    while True:
        recurse_lookups = sum(
            (self.Lookup[i].collect_lookups() for i in recurse if i < self.LookupCount),
            [],
        )
        recurse_lookups = [
            l
            for l in recurse_lookups
            if l not in lookup_indices and l < self.LookupCount
        ]
        if not recurse_lookups:
            return _uniq_sort(lookup_indices)
        recurse_lookups = _uniq_sort(recurse_lookups)
        lookup_indices.extend(recurse_lookups)
        recurse = recurse_lookups

