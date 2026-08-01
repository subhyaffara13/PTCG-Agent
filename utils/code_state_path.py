
def code_state_path(cache_key: str) -> str | None:
    if not torch._dynamo.config.automatic_dynamic_local_pgo:
        log.debug("automatic_dynamic_local_pgo not enabled")
        return None

    from torch._inductor.runtime.runtime_utils import cache_dir

    code_state_key = re.sub(r'[<>:"/\\|?*]', "_", f"code_state_{cache_key}.pkl")
    return os.path.join(cache_dir(), "dynamo", code_state_key)

