
def remap_duplicate_features(self, feature_indices):
    """Return retained feature indices(without duplicates) and remapped feature indices"""
    features = self.table.FeatureList.FeatureRecord

    unique_features = {}
    duplicate_features = {}
    for i in feature_indices:
        f = features[i]
        tag = f.FeatureTag

        same_tag_features = unique_features.get(tag)
        if same_tag_features is None:
            unique_features[tag] = set([i])
            duplicate_features[i] = i
            continue

        found = False
        for other_i in same_tag_features:
            if features[other_i] == f:
                found = True
                duplicate_features[i] = other_i
                break

        if not found:
            same_tag_features.add(i)
            duplicate_features[i] = i

    ## remap retained feature indices
    feature_map = {}
    new_idx = 0

    for i in feature_indices:
        unique_i = duplicate_features.get(i, i)
        v = feature_map.get(unique_i)
        if v is None:
            feature_map[i] = new_idx
            new_idx += 1
        else:
            feature_map[i] = v

    retained_feature_indices = _uniq_sort(
        sum((list(s) for s in unique_features.values()), [])
    )
    return (retained_feature_indices, feature_map)

