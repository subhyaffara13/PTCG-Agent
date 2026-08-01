
def flatten_ids(ids):
    collapse = lambda acc, an_id: acc + sorted(an_id.equivalent_ids,
                                        key=default_sort_key)
    ids = reduce(collapse, ids, [])
    ids.sort(key=default_sort_key)
    return ids

