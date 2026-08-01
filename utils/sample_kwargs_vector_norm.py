
def sample_kwargs_vector_norm(t, **kwargs):
    # orders with / without identity
    def ords():
        has_id = (6, 4, 2, 1, 0, 0.9)
        no_id = (inf, -2.1, -inf)
        if t.numel() == 0:
            dim = kwargs.get("dim")
            if dim is None:
                return has_id
            if not isinstance(dim, Iterable):
                dim = (dim,)
            for d in dim:
                if t.size(d) == 0:
                    return has_id
        return has_id + no_id

    return (((), dict(ord=o)) for o in ords())

