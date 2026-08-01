
def randomize(args):
    def transform(x):
        if not x.dtype.is_floating_point:
            return x
        return x.detach().clone().uniform_(0, 1).requires_grad_(x.requires_grad)
    return pytree.tree_map_only(torch.Tensor, transform, args)

