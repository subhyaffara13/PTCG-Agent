
def op_region_builder(op, op_region, terminator=None):
    def builder_wrapper(body_builder):
        # Add a block with block args having types determined by type hints on the wrapped function.
        if len(op_region.blocks) == 0:
            sig = inspect.signature(body_builder)
            types = [p.annotation for p in sig.parameters.values()]
            if not (
                len(types) == len(sig.parameters)
                and all(isinstance(t, Type) for t in types)
            ):
                raise ValueError(
                    f"for {body_builder=} either missing a type annotation or type annotation isn't a mlir type: {sig}"
                )

            op_region.blocks.append(*types)

        with InsertionPoint(op_region.blocks[0]):
            results = body_builder(*list(op_region.blocks[0].arguments))

        with InsertionPoint(list(op_region.blocks)[-1]):
            if terminator is not None:
                res = []
                if isinstance(results, (tuple, list)):
                    res.extend(results)
                elif results is not None:
                    res.append(results)
                terminator(res)

        return get_op_result_or_op_results(op)

    return builder_wrapper

