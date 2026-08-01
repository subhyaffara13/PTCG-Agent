
def is_general_tensor_shape_node(node, modules):
    func_list = [
        torch.narrow,
        torch.transpose,
        torch.repeat_interleave,
        torch.squeeze,
        torch.stack,
        torch.unsqueeze,
        torch.nn.functional.pixel_shuffle,
        torch.nn.functional.pixel_unshuffle,
    ]
    method_list = [
        "contiguous",
        "detach",
        "detach_",
        "permute",
        "repeat",
        "repeat_interleave",
        "reshape",
        "resize_",
        "shape",
        "size",
        "squeeze",
        "squeeze_",
        "transpose",
        "unsqueeze",
        "unsqueeze_",
        "view",
    ]
    module_type_list = [
        torch.nn.Identity,
        torch.nn.PixelShuffle,
        torch.nn.PixelUnshuffle,
    ]
    return _is_node_in_list(node, modules, func_list, method_list, module_type_list)

