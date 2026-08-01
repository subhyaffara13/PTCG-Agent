
def get_ir_cache_name(id: str, path: str, options: Options) -> str:
    meta_path, _, _ = get_cache_names(id, path, options)
    # Mypyc uses JSON cache even with --fixed-format-cache (for now).
    return meta_path.replace(".meta.json", ".ir.json").replace(".meta.ff", ".ir.json")

