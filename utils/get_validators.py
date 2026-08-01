
def get_validators() -> tuple[str, str]:
    r"""Return the TunableOp validators."""
    return torch._C._cuda_tunableop_get_validators()  # type: ignore[attr-defined]


def get_validators() -> list[Validator]:
    return [
        num_examples_validator,
        lambda x: necessary_column_validator(x, "prompt"),
        lambda x: necessary_column_validator(x, "completion"),
        additional_column_validator,
        non_empty_field_validator,
        format_inferrer_validator,
        duplicated_rows_validator,
        long_examples_validator,
        lambda x: lower_case_validator(x, "prompt"),
        lambda x: lower_case_validator(x, "completion"),
        common_prompt_suffix_validator,
        common_prompt_prefix_validator,
        common_completion_prefix_validator,
        common_completion_suffix_validator,
        completions_space_start_validator,
    ]

