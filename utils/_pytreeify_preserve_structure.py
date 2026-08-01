
def _pytreeify_preserve_structure(f):
    @wraps(f)
    def nf(args):
        flat_args, spec = tree_flatten(args)
        out = f(*flat_args)
        return tree_unflatten(out, spec)

    return nf

