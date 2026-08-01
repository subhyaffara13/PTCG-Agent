
def disable_inference_mode_for_fake_prop() -> Generator[None, None, None]:
    prior = getattr(tls, "disable_inference_mode", False)
    tls.disable_inference_mode = True
    try:
        yield
    finally:
        tls.disable_inference_mode = prior

