import functools

def addmm_patterns_init():
    """
    addmm related patterns.
    To avoid duplication, also includes int8 WoQ GEMM pattern without bias.
    """
    device = next(
        (gpu for gpu in GPU_TYPES if getattr(torch, gpu).is_available()), "cpu"
    )
    val = functools.partial(torch.empty, (10, 10), device=device, requires_grad=False)
    scale = functools.partial(torch.empty, (10,), device=device, requires_grad=False)

    def check_int8_woq_concat_linear_weights(match):
        is_cpu = match.kwargs["inp"].meta["val"].is_cpu
        if not is_cpu or not config.cpp.enable_concat_linear:
            # Currently, this pattern is only supported on CPU
            return False

        weight_inputs = ["w1", "w2"]
        if "w3" in match.kwargs:
            weight_inputs.append("w3")

        if not all(
            match.kwargs[wgt].target is torch.ops.prims.convert_element_type.default
            for wgt in weight_inputs
        ):
            return False

        if not all(
            next(iter(match.kwargs[wgt]._input_nodes.keys())).meta["val"].dtype
            is torch.int8
            for wgt in weight_inputs
        ):
            return False

        if not all(
            match.kwargs[wgt].meta["val"].dtype is torch.bfloat16
            for wgt in weight_inputs
        ):
            return False

        return True

    def check_concat_weights(match):
        is_cpu = match.kwargs["inp"].meta["val"].is_cpu
        if is_cpu and not config.cpp.enable_concat_linear:
            return False

        weight_inputs = ["w1", "w2"]
        if "w3" in match.kwargs:
            weight_inputs.append("w3")

        equal_shape_inputs = [weight_inputs]

        if "b1" in match.kwargs:
            bias_inputs = ["b1", "b2"]
            if "b3" in match.kwargs:
                bias_inputs.append("b3")

            equal_shape_inputs.append(bias_inputs)

        for equal_shape_group in equal_shape_inputs:
            inps = [match.kwargs[name] for name in equal_shape_group]

            if not all(
                inp.op == "get_attr"
                and inp.meta["val"].shape[:-1] == inps[0].meta["val"].shape[:-1]
                for inp in inps
            ):
                return False
        return True

    def int8_woq_fusion_pattern(inp, w1, w2, w3, s1, s2, s3):
        return ((inp @ w1) * s1, (inp @ w2) * s2, (inp @ w3) * s3)

    def int8_woq_fusion_replacement(inp, w1, w2, w3, s1, s2, s3):
        cat_w = torch.cat((w1, w2, w3), dim=1)
        cat_s = torch.cat((s1, s2, s3), dim=0)
        mm = (inp @ cat_w).mul(cat_s)
        n1, n2 = w1.size(1), w2.size(1)
        return mm.tensor_split([n1, n1 + n2], dim=-1)

    register_replacement(
        # pyrefly: ignore [bad-argument-type]
        int8_woq_fusion_pattern,
        # pyrefly: ignore [bad-argument-type]
        int8_woq_fusion_replacement,
        [val(), val(), val(), val(), scale(), scale(), scale()],
        # pyrefly: ignore [bad-argument-type]
        fwd_only,
        # pyrefly: ignore [bad-argument-type]
        pass_patterns[0],
        extra_check=check_int8_woq_concat_linear_weights,
        exclusive_arg_names=("w1", "w2", "w3", "s1", "s2", "s3"),
    )

    def matmul_fuse_pattern(inp, w1, w2, w3):
        return (inp @ w1, inp @ w2, inp @ w3)

    def matmul_replacement(inp, w1, w2, w3):
        weights = (w1, w2, w3)
        cat_t = torch.cat(weights, dim=1)
        mm = inp @ cat_t
        return mm.split([w.size(1) for w in weights], dim=1)

    register_replacement(
        # pyrefly: ignore [bad-argument-type]
        matmul_fuse_pattern,
        # pyrefly: ignore [bad-argument-type]
        matmul_replacement,
        [val(), val(), val(), val()],
        # pyrefly: ignore [bad-argument-type]
        fwd_only,
        # pyrefly: ignore [bad-argument-type]
        pass_patterns[0],
        extra_check=check_concat_weights,
        exclusive_arg_names=("w1", "w2", "w3"),
    )

    def matmul_fuse_pattern_two(inp, w1, w2):
        return (inp @ w1, inp @ w2)

    def matmul_replacement_two(inp, w1, w2):
        weights = (w1, w2)
        cat_t = torch.cat(weights, dim=1)
        mm = inp @ cat_t
        return mm.split([w.size(1) for w in weights], dim=1)

    register_replacement(
        # pyrefly: ignore [bad-argument-type]
        matmul_fuse_pattern_two,
        # pyrefly: ignore [bad-argument-type]
        matmul_replacement_two,
        [val(), val(), val()],
        # pyrefly: ignore [bad-argument-type]
        fwd_only,
        # pyrefly: ignore [bad-argument-type]
        pass_patterns[0],
        extra_check=check_concat_weights,
        exclusive_arg_names=("w1", "w2"),
    )

    def addmm_fuse_pattern_second(inp, w1, w2, w3, b1, b2, b3):
        return (
            aten.addmm(b1, inp, w1),
            aten.addmm(b2, inp, w2),
            aten.addmm(b3, inp, w3),
        )

    def addmm_fuse_replacement_second(inp, w1, w2, w3, b1, b2, b3):
        weights = (w1, w2, w3)
        cat_w = torch.cat(weights, dim=1)
        cat_b = torch.cat((b1, b2, b3))
        return aten.addmm(cat_b, inp, cat_w).split([w.size(1) for w in weights], dim=1)

    register_replacement(
        # pyrefly: ignore [bad-argument-type]
        addmm_fuse_pattern_second,
        # pyrefly: ignore [bad-argument-type]
        addmm_fuse_replacement_second,
        [val() for _ in range(7)],
        # pyrefly: ignore [bad-argument-type]
        fwd_only,
        # pyrefly: ignore [bad-argument-type]
        pass_patterns[0],
        extra_check=check_concat_weights,
        exclusive_arg_names=("w1", "w2", "w3", "b1", "b2", "b3"),
    )

