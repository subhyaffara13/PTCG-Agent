
def _feature_variations_tags(ds):
    raw_tags = ds.lib.get(
        FEAVAR_FEATURETAG_LIB_KEY,
        "rclt" if ds.rulesProcessingLast else "rvrn",
    )
    return sorted({t.strip() for t in raw_tags.split(",")})

