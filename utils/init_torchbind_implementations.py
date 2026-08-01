
def init_torchbind_implementations():
    global _TORCHBIND_IMPLS_INITIALIZED
    global _TENSOR_QUEUE_GLOBAL_TEST
    if _TORCHBIND_IMPLS_INITIALIZED:
        return

    load_torchbind_test_lib()
    register_fake_operators()
    register_fake_classes()
    _TENSOR_QUEUE_GLOBAL_TEST = _empty_tensor_queue()
    _TORCHBIND_IMPLS_INITIALIZED = True

