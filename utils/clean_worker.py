
def clean_worker(*args, **kwargs):
    import gc

    multiprocessing.pool.worker(*args, **kwargs)
    # Regular multiprocessing workers don't fully clean up after themselves,
    # so we have to explicitly trigger garbage collection to make sure that all
    # destructors are called...
    gc.collect()

