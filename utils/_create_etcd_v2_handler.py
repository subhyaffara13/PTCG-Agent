
def _create_etcd_v2_handler(params: RendezvousParameters) -> RendezvousHandler:
    from .etcd_rendezvous_backend import create_backend

    backend, store = create_backend(params)

    return create_handler(store, backend, params)

