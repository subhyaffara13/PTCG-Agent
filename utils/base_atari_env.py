
def BaseAtariEnv(**kwargs):
    return parallel_to_aec_wrapper(ParallelAtariEnv(**kwargs))

