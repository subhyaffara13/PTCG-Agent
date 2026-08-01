
def _get_global_app() -> WebhooksServer:  # ty: ignore[invalid-type-form]
    global _global_app
    if _global_app is None:
        _global_app = WebhooksServer()
    return _global_app

