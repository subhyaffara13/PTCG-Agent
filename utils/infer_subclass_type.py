
def infer_subclass_type(value: T) -> type[T] | None:
    if type(value) in (
        torch.Tensor,
        torch.nn.Parameter,
        torch._subclasses.fake_tensor.FakeTensor,
        torch._subclasses.functional_tensor.FunctionalTensor,
    ) or is_traceable_wrapper_subclass(value):
        # Ordinarily, we would fakeify a tensor so that it can get dynamic
        # shapes and be computed on without triggering actual operations.
        # However, how can we fakeify a tensor subclass?  Ordinary
        # inheritance (nor multiple inheritance) won't work work.
        #
        # Instead, our plan is to *manually simulate* the tensor subclass
        # inheriting from a fake tensor with dynamo.  This means our
        # data representation for a tensor subclass will be a fake tensor
        # + tensor subclass type + any extra data the subclass may have
        # been storing on the tensor.  Because all Python accesses are
        # mediated through TensorWithTFOverrideVariable, we can ensure
        # that we dispatch differently, e.g., according to
        # __torch_function__
        #
        # To simplify things for now, the __dict__ tracking bits haven't
        # been implemented yet, but they can be added into this design at
        # a later point in time.
        return None
    else:
        return type(value)

