
def route(method: str, path: str, handler: _HandlerType, **kwargs: Any) -> RouteDef:
    return RouteDef(method, path, handler, kwargs)

