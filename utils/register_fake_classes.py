
def register_fake_classes():
    # noqa: F841
    @torch._library.register_fake_class("_TorchScriptTesting::_Foo")
    class FakeFoo:
        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y

        @classmethod
        def __obj_unflatten__(cls, flattend_foo):
            return cls(**dict(flattend_foo))

        def add_tensor(self, z):
            return (self.x + self.y) * z

    @torch._library.register_fake_class("_TorchScriptTesting::_ContainsTensor")
    class FakeContainsTensor:
        def __init__(self, t: torch.Tensor):
            self.t = t

        @classmethod
        def __obj_unflatten__(cls, flattend_foo):
            return cls(**dict(flattend_foo))

        def get(self):
            return self.t

    @torch._library.register_fake_class("_TorchScriptTesting::_TensorQueue")
    class FakeTensorQueue:
        def __init__(self, queue):
            self.queue = queue

        @classmethod
        def __obj_unflatten__(cls, flattened_ctx):
            return cls(**dict(flattened_ctx))

        def push(self, x):
            self.queue.append(x)

        def pop(self):
            if self.is_empty():
                return torch.empty([])
            return self.queue.pop(0)

        def size(self):
            return len(self.queue)

        def is_empty(self):
            return len(self.queue) == 0

        def float_size(self):
            return float(len(self.queue))

    @torch._library.register_fake_class("_TorchScriptTesting::_FlattenWithTensorOp")
    class FakeFlatten:
        def __init__(self, t):
            self.t = t

        def get(self):
            return self.t

        @classmethod
        def __obj_unflatten__(cls, flattened_ctx):
            return cls(**dict(flattened_ctx))

