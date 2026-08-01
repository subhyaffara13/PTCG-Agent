
def force_lazy_device(model: fx.GraphModule):
    """
    Factory methods in a Fx graph may create tensors for a specific eager devices.
    If we take no actions, those eager tensors will be mixed with lazy tensors and
    cause crash. This method overwrite those eager device to lazy device.
    """

    def tolazydevice(dev):
        if isinstance(dev, torch.device):
            return torch.device("lazy", index=dev.index)
        return dev

    def hasDeviceArg(args, kwargs):
        return any(
            isinstance(arg, torch.device)
            for arg in itertools.chain(args, kwargs.values())
        )

    for nd in model.graph.nodes:
        nd.args = tuple(tolazydevice(arg) for arg in nd.args)
        nd.kwargs = {k: tolazydevice(v) for k, v in nd.kwargs.items()}

        # For torchbench like yolov3, hf_Bart, dynamo generates Fx graph that return
        # eager tensors on the default device
        # (check https://gist.github.com/shunting314/eabdf6c769c59bc384469717b8f9bb7f for yolove,
        # and https://gist.github.com/shunting314/8d5e2d9348a3258959d3954186c48814 for hf_Bart).
        # To force those tensors on the lazy device, we can not simply override
        # the device argument since there is no explicit device argument.
        # What we are doing here is, for the list of covered tensor factory methods
        # we add a lazy device argument explicitly.
        #
        # TODO: This solution is no ideal since we may miss some factory methods. In future
        # when we support lazy mode, this method can be replaced by that.
        if nd.target in tensor_factory_functions and not hasDeviceArg(
            nd.args, nd.kwargs
        ):
            kwargs = dict(nd.kwargs)  # nd.kwargs is immutable. make a mutable copy.
            kwargs["device"] = torch.device("lazy")
            nd.kwargs = kwargs

    model.recompile()

