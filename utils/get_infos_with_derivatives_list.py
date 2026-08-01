
def get_infos_with_derivatives_list(
    differentiability_infos: dict[FunctionSchema, dict[str, DifferentiabilityInfo]],
) -> list[DifferentiabilityInfo]:
    diff_info_list = [
        info
        for diffinfo_dict in differentiability_infos.values()
        for info in diffinfo_dict.values()
    ]

    return list(filter(lambda info: info.args_with_derivatives, diff_info_list))

