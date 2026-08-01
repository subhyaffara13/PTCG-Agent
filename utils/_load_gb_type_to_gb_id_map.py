
def _load_gb_type_to_gb_id_map() -> dict[str, Any]:
    """
    Loads the gb_type to gb_id map from the graph break registry from JSON file with caching.

    Includes historical gb_type (mapping behavior of duplicate gb_types with different gb_ids is undefined).
    """
    try:
        script_dir = Path(__file__).resolve().parent
        registry_path = get_file_path_2(
            "", str(script_dir), "graph_break_registry.json"
        )
        with open(registry_path) as f:
            registry = json.load(f)
    except Exception:
        log.exception("Error accessing the registry file")
        # pyrefly: ignore [implicit-any]
        registry = {}

    mapping = {}
    for k, v in registry.items():
        for entry in v:
            mapping[entry["Gb_type"]] = k

    return mapping

