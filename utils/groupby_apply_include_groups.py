
def groupby_apply_include_groups(val):
    if _version_predates(pd, "2.2.0"):
        return {}
    return {"include_groups": val}

