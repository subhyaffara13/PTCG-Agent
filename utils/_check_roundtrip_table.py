
def _check_roundtrip_table(obj, comparator, path, compression=False):
    options = {}
    if compression:
        options["complib"] = "blosc"

    with HDFStore(path, "w", **options) as store:
        store.put("obj", obj, format="table")
        retrieved = store["obj"]

        comparator(retrieved, obj)

