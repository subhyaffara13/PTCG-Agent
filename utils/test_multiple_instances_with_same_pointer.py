
def test_multiple_instances_with_same_pointer():
    n = 100
    instances = [m.SamePointer() for _ in range(n)]
    for i in range(n):
        # We need to reuse the same allocated memory for with a different type,
        # to ensure the bug in `deregister_instance_impl` is detected. Otherwise
        # `Py_TYPE(self) == Py_TYPE(it->second)` will still succeed, even though
        # the `instance` is already deleted.
        instances[i] = m.Empty()

