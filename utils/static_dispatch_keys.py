
def static_dispatch_keys(backends: list[BackendIndex]) -> list[DispatchKey]:
    if len(backends) == 0:
        return []
    else:
        return [backend.dispatch_key for backend in backends] + [
            DispatchKey.CompositeImplicitAutograd,
            DispatchKey.CompositeImplicitAutogradNestedTensor,
            DispatchKey.CompositeExplicitAutograd,
            DispatchKey.CompositeExplicitAutogradNonFunctional,
        ]

