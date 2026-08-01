
def check_meta_consistency(
    lhs_list: list[torch.Tensor | torch.SymInt | int],
    rhs_list: list[torch.Tensor | torch.SymInt | int],
    lhs_name: str,
    rhs_name: str,
    include_contiguity: bool = True,
) -> None:
    def diff_meta_pairs(
        lhs_list: list[torch.Tensor | torch.SymInt | int],
        rhs_list: list[torch.Tensor | torch.SymInt | int],
    ) -> list[str]:
        def diff_meta(
            lhs: torch.Tensor | torch.SymInt | int,
            rhs: torch.Tensor | torch.SymInt | int,
        ) -> str:
            if isinstance(lhs, torch.Tensor) and isinstance(rhs, torch.Tensor):
                return ", ".join(
                    diff_tensor_meta(
                        _extract_tensor_metadata(
                            lhs, include_contiguity=include_contiguity
                        ),
                        _extract_tensor_metadata(
                            rhs, include_contiguity=include_contiguity
                        ),
                        check_grad=False,
                    )
                )
            else:

                def _both_int_types(lhs, rhs):
                    return isinstance(lhs, (int, torch.SymInt)) and isinstance(
                        rhs, (int, torch.SymInt)
                    )

                def _both_tensor(lhs, rhs):
                    return isinstance(lhs, torch.Tensor) and isinstance(
                        rhs, torch.Tensor
                    )

                if not _both_int_types(lhs, rhs) and not _both_tensor(lhs, rhs):
                    return f"type: {lhs} vs {rhs}"

            return ""

        # Manually check the device of lhs and rhs as this field is currently not part of TensorMetadata
        def diff_device(
            lhs: torch.Tensor | torch.SymInt | int,
            rhs: torch.Tensor | torch.SymInt | int,
        ) -> str:
            if isinstance(lhs, torch.Tensor) and isinstance(rhs, torch.Tensor):
                if (
                    rhs.device.type == lhs.device.type
                    and rhs.device.index == lhs.device.index
                ):
                    return ""
                else:
                    return "device"
            return ""

        if len(lhs_list) != len(rhs_list):
            raise torch._dynamo.exc.UncapturedHigherOrderOpError(
                f"Expected {lhs_name} and {rhs_name} to have same number of outputs but got lhs:{lhs_list} and rhs:{rhs_list}"
            )
        all_diffs = []
        for i, (lhs, rhs) in enumerate(zip(lhs_list, rhs_list)):
            if diff := diff_meta(lhs, rhs):
                all_diffs.append(
                    f"pair[{i}] differ in {diff}, where lhs is {lhs} and rhs is {rhs}"
                )
            if diff := diff_device(lhs, rhs):
                all_diffs.append(
                    f"pair[{i}] differ in {diff}, where lhs is {lhs} and rhs is {rhs}"
                )
        return all_diffs

    if all_diffs := diff_meta_pairs(lhs_list, rhs_list):
        diff_str = "\n".join(all_diffs)
        raise torch._dynamo.exc.UncapturedHigherOrderOpError(
            f"Expected {lhs_name} and {rhs_name} to have same metadata but found:\n{diff_str}"
        )

