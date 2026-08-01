
def _sfdp_extra_check(scale_factor_op=None, disable_cuda=False):
    def fn(match):
        if (
            disable_cuda
            and "query" in match.kwargs
            and "cuda" in str(match.kwargs["query"].meta["val"].device)
        ):
            return False
        if scale_factor_op is not None:
            scale_factor_node = filter_nodes(match.nodes, scale_factor_op)[0]
            # Note: args[1] of the scale_factor_node is always the scale_factor for the current patterns.
            scale_factor = scale_factor_node.args[1]
            # make sure the scale_factor a float/int. SymInt?
            if not isinstance(scale_factor, (float, int)):
                return False
        return _sfdp_params_check(match)

    return fn

