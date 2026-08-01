
def tuned_baddbmm(inp, mat1, mat2, *, alpha=1, beta=1, layout=None):
    """
    Lowering for autotuning aten.mm with different backends (Aten, Triton, CUTLASS, etc.)
    """
    if use_native_matmul(mat1, mat2):
        if beta == 0:
            arg1 = 0
        else:
            arg1 = lowerings[aten.mul](beta, inp)

        if alpha == 0:
            arg2 = 0
        else:
            arg2 = lowerings[aten.mul](alpha, lowerings[aten.bmm](mat1, mat2))

        return lowerings[aten.add](arg1, arg2)

    # TODO(coconutruben): integrate into MMKernelInputs when all callsites use that
    m, n, k, layout, mat1, mat2, inp = mm_args(mat1, mat2, inp, layout=layout)

    # Create MMKernelInputs for BadDBMM at the top
    kernel_inputs = MMKernelInputs(
        [inp, mat1, mat2], scalars=dict(alpha=alpha, beta=beta)
    )

    # below is for getting an overview logging info of inductor mms
    batch_size = mat1.get_size()[0]
    counters["aten_mm_info"][f"aten.baddbmm_{batch_size}_{m}_{n}_{k}"] += 1
    log.info(
        "Tuned aten.baddbmm: batch_size=%s, m=%s, n=%s, k=%s, mat1_dtype=%s, mat2_dtype=%s, inp=%s, output_layout=%s",
        batch_size,
        m,
        n,
        k,
        mat1.get_dtype(),
        mat2.get_dtype(),
        inp.get_dtype(),
        layout,
    )
    name = "baddbmm"
    # options to tune from
    choices: list[ChoiceCaller] = []

    # Collect all templates for unified call
    templates_to_use: list[ExternKernelChoice | KernelTemplate] = []
    if use_aten_gemm_kernels():
        templates_to_use.append(aten_baddbmm)

    if use_triton_template(layout, check_max_autotune=False):
        templates_to_use.append(bmm_template)

    # Single unified call for all templates
    choices.extend(
        V.choices.get_template_configs(kernel_inputs, templates_to_use, name)
    )

    node, _ = autotune_select_algorithm(name, choices, kernel_inputs.nodes(), layout)
    return node

