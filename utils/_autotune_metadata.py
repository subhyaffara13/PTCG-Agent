
def _autotune_metadata(input_nodes):
    """Helper function to extract autotune metadata from input nodes."""
    return {
        "autotune_strides": ", ".join([str(n.get_stride()) for n in input_nodes]),
        "autotune_dtypes": ", ".join([str(n.get_dtype()) for n in input_nodes]),
        "autotune_shape": ", ".join(
            ["x".join(map(str, n.get_size())) for n in input_nodes]
        ),
        "autotune_offset": ", ".join([str(n.get_layout().offset) for n in input_nodes]),
        # TODO(coconutruben): replace this with taking KernelInputs as the
        # argument, and extracting those out there directly
        "autotune_strides_hinted": ", ".join(
            [
                str(V.graph.sizevars.optimization_hints(n.get_stride()))
                for n in input_nodes
            ]
        ),
        "autotune_shape_hinted": ", ".join(
            [
                "x".join(
                    map(
                        str,
                        V.graph.sizevars.optimization_hints(n.get_size()),
                    )
                )
                for n in input_nodes
            ]
        ),
    }

