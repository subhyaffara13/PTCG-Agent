
def update_callable_ids(c: CallableType, ids: list[TypeVarId]) -> CallableType:
    tv_map = {}
    tvs = []
    for tv, new_id in zip(c.variables, ids):
        new_tv = tv.copy_modified(id=new_id)
        tvs.append(new_tv)
        tv_map[tv.id] = new_tv
    return expand_type(c, tv_map).copy_modified(variables=tvs)

