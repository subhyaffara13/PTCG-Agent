
def use_numpy_random():
    # local import to avoid ref cycles
    import torch._dynamo.config as config

    return config.use_numpy_random_stream

