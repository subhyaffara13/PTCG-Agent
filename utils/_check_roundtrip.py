
def _check_roundtrip(obj, comparator, path, compression=False, **kwargs):
    options = {}
    if compression:
        options["complib"] = "blosc"

    with HDFStore(path, "w", **options) as store:
        store["obj"] = obj
        retrieved = store["obj"]
        comparator(retrieved, obj, **kwargs)

