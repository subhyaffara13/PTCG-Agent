
def override_qengines(qfunction):
    def test_fn(*args, **kwargs):
        for qengine in supported_qengines:
            with override_quantized_engine(qengine):
                # qfunction should not return anything.
                qfunction(*args, **kwargs)
    return test_fn

