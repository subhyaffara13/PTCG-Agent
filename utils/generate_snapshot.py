
def generate_snapshot() -> Dict[str, Dict]:
    import importlib

    from fastapi.openapi.utils import get_openapi

    from litellm.proxy._lazy_features import LAZY_FEATURES
    from litellm.proxy.proxy_server import app, ensure_unique_openapi_operation_ids

    for feat in LAZY_FEATURES:
        if feat.module_path in sys.modules:
            continue
        try:
            module = importlib.import_module(feat.module_path)
            feat.register_fn(app, module)
        except Exception as exc:
            sys.stderr.write(f"warning: skip {feat.name}: {exc}\n")

    fragments: Dict[str, Dict] = {}
    used_operation_ids: Set[str] = set()
    for feat in LAZY_FEATURES:
        feat_routes = [
            r
            for r in app.routes
            if any(getattr(r, "path", "").startswith(p) for p in feat.path_prefixes)
        ]
        if not feat_routes:
            continue
        _stabilize_multi_method_route_ids(feat_routes)
        full = get_openapi(title=app.title, version=app.version, routes=feat_routes)
        paths = full.get("paths", {})
        _normalize_operation_ids(paths)
        # Group all of a feature's routes under one tag.
        for path_ops in full.get("paths", {}).values():
            for method, op in path_ops.items():
                if isinstance(op, dict):
                    operation_id = op.get("operationId")
                    if isinstance(operation_id, str):
                        for suffix in HTTP_METHOD_SUFFIXES:
                            if operation_id.endswith(f"_{suffix}"):
                                op["operationId"] = (
                                    operation_id[: -len(suffix)] + method
                                )
                                break
                    op["tags"] = [feat.name]
        full = ensure_unique_openapi_operation_ids(full, used_operation_ids)
        fragments[feat.name] = {
            "paths": paths,
            "components": {"schemas": full.get("components", {}).get("schemas", {})},
        }
    return fragments

