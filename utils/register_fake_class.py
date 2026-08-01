
def register_fake_class(qualname, fake_class: HasStaticMethodFromReal | None = None):
    r"""Register a fake implementation for this class.

    It's in the same spirit of registering a fake implementation for
    an operator but with the difference that it
    associates a fake class with the original torch bind class (registered
    with torch::class_). In this way, torch.compile can handle them properly
    in components such as Dynamo and AOTAutograd.

    This API may be used as a decorator (see example). For the fake class, users
    are required to provide a from_real classmethod that takes a real object and
    returns an instance of the fake class. All tensors in the fake object should also
    be properly fakified with to_fake_tensor() in from_real.


    Examples:
        # For a custom class Foo defined in test_custom_class_registration.cpp:

        TORCH_LIBRARY(_TorchScriptTesting, m) {
          m.class_<TensorQueue>("_TensorQueue")
            .def(torch::init<at::Tensor>())
            .def("push", &TensorQueue::push)
            .def("pop", &TensorQueue::pop)
            .def("top", &TensorQueue::top)
            .def("size", &TensorQueue::size)
            .def("clone_queue", &TensorQueue::clone_queue)
            .def("__obj_flatten__", &TensorQueue::__obj_flatten__)
            .def_pickle(
                // __getstate__
                [](const c10::intrusive_ptr<TensorQueue>& self)
                    -> c10::Dict<std::string, at::Tensor> {
                  return self->serialize();
                },
                // __setstate__
                [](c10::Dict<std::string, at::Tensor> data)
                    -> c10::intrusive_ptr<TensorQueue> {
                  return c10::make_intrusive<TensorQueue>(std::move(data));
                });
            };
        # We could register a fake class FakeTensorQueue in Python as follows:
        import torch

        @torch._library.register_fake_class("_TorchScriptTesting::_TensorQueue")
        class FakeTensorQueue:
            def __init__(self, queue):
                self.queue = queue

            @classmethod
            def __obj_unflatten__(cls, flattened_ctx):
                return cls(**dict(ctx))

            def push(self, x):
                self.queue.append(x)

            def pop(self):
                return self.queue.pop(0)

            def size(self):
                return len(self.queue)

    In this example, the original TensorQeue need to add a __obj_flatten__ method
    to the class TensorQueue and the flattened result is passed into FakeTensorQueue's
    __obj_unflatten__ as inputs to create a fake class. This protocol allows pytorch to look
    at the contents of the script object and properly handle them in the subsystems
    like dynamo, aot_aotugrad or more.
    """

    def inner(fake_class: HasStaticMethodFromReal):
        ns, name = parse_namespace(qualname)

        # This also checks whether the referred torch::class_ exists.
        torch._C._get_custom_class_python_wrapper(ns, name)

        from_method = getattr(fake_class, _CONVERT_FROM_REAL_NAME, None)
        if not from_method:
            raise RuntimeError(
                f"{fake_class} doesn't define a classmethod {_CONVERT_FROM_REAL_NAME}."
            )

        if not isinstance(fake_class.__dict__[_CONVERT_FROM_REAL_NAME], classmethod):
            raise RuntimeError(
                f"{_CONVERT_FROM_REAL_NAME} method is not a classmethod."
            )

        global_fake_class_registry.register(_full_qual_class_name(qualname), fake_class)
        return fake_class

    if fake_class is None:
        return inner
    return inner(fake_class)

