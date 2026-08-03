import json

def load_scc_from_cache(
    scc: list[MypyFile], result: BuildResult, mapper: Mapper, ctx: DeserMaps
) -> ModuleIRs:
    """Load IR for an SCC of modules from the cache.

    Arguments and return are as compile_scc_to_ir.
    """
    cache_data = {
        k.fullname: json.loads(
            result.manager.metastore.read(get_state_ir_cache_name(result.graph[k.fullname]))
        )["ir"]
        for k in scc
    }
    modules = deserialize_modules(cache_data, ctx)
    load_type_map(mapper, scc, ctx)
    return modules

