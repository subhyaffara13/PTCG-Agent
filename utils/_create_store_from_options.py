
def _create_store_from_options(backend_options, rank):
    store, _, _ = next(_rendezvous_helper(backend_options.init_method, rank, None))
    return store

