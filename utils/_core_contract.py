from typing import Any, Optional, Union

def _core_contract(
    operands_: Sequence[ArrayType],
    contraction_list: ContractionListType,
    backend: Optional[str] = "auto",
    evaluate_constants: bool = False,
    out: Optional[ArrayType] = None,
    **kwargs: Any,
) -> ArrayType:
    """Inner loop used to perform an actual contraction given the output
    from a ``contract_path(..., einsum_call=True)`` call.
    """
    # Special handling if out is specified
    specified_out = out is not None

    operands = list(operands_)
    backend = parse_backend(operands, backend)

    # try and do as much as possible without einsum if not available
    no_einsum = not backends.has_einsum(backend)

    # Start contraction loop
    for num, contraction in enumerate(contraction_list):
        inds, idx_rm, einsum_str, _, blas_flag = contraction

        # check if we are performing the pre-pass of an expression with constants,
        #     if so, break out upon finding first non-constant (None) operand
        if evaluate_constants and any(operands[x] is None for x in inds):
            return operands, contraction_list[num:]

        tmp_operands = [operands.pop(x) for x in inds]

        # Do we need to deal with the output?
        handle_out = specified_out and ((num + 1) == len(contraction_list))

        # Call tensordot (check if should prefer einsum, but only if available)
        if blas_flag and ("EINSUM" not in blas_flag or no_einsum):  # type: ignore
            # Checks have already been handled
            input_str, results_index = einsum_str.split("->")
            input_left, input_right = input_str.split(",")

            tensor_result = "".join(s for s in input_left + input_right if s not in idx_rm)

            if idx_rm:
                # Find indices to contract over
                left_pos, right_pos = [], []
                for s in idx_rm:
                    left_pos.append(input_left.find(s))
                    right_pos.append(input_right.find(s))

                # Construct the axes tuples in a canonical order
                axes = tuple(zip(*sorted(zip(left_pos, right_pos))))
            else:
                # Ensure axes is always pair of tuples
                axes = ((), ())

            # Contract!
            new_view = _tensordot(*tmp_operands, axes=axes, backend=backend, **kwargs)

            # Build a new view if needed
            if (tensor_result != results_index) or handle_out:
                transpose = tuple(map(tensor_result.index, results_index))
                new_view = _transpose(new_view, axes=transpose, backend=backend)

                if handle_out:
                    out[:] = new_view  # type: ignore

        else:
            # Call einsum
            out_kwarg: Union[None, ArrayType] = None
            if handle_out:
                out_kwarg = out
            new_view = _einsum(einsum_str, *tmp_operands, backend=backend, out=out_kwarg, **kwargs)

        # Append new items and dereference what we can
        operands.append(new_view)
        del tmp_operands, new_view

    if specified_out:
        return out
    else:
        return operands[0]

