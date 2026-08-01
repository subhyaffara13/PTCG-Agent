
def init_reductions():
    reduction.register(torch.cuda.Event, reduce_event)

    for t in torch._storage_classes:
        if t.__name__ == "UntypedStorage":
            reduction.register(t, reduce_storage)
        else:
            reduction.register(t, reduce_typed_storage_child)

    reduction.register(torch.storage.TypedStorage, reduce_typed_storage)

    for t in torch._tensor_classes:
        reduction.register(t, reduce_tensor)

    # TODO: Maybe this should be in tensor_classes? :)
    reduction.register(torch.Tensor, reduce_tensor)

    from torch.nn.parameter import Parameter

    reduction.register(Parameter, reduce_tensor)

