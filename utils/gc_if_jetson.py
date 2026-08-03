import functools

def gcIfJetson(fn):
    # Irregular Jetson host/device memory setup requires cleanup to avoid tests being killed
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if IS_JETSON:
            gc.collect()
            torch.cuda.empty_cache()
        fn(*args, **kwargs)
    return wrapper

