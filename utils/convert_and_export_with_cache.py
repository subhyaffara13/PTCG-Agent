
def convert_and_export_with_cache(
    model: PreTrainedModel,
    example_input_ids: torch.Tensor | None = None,
    example_cache_position: torch.Tensor | None = None,
    dynamic_shapes: dict | None = None,
    strict: bool | None = None,
):
    """
    Convert a `PreTrainedModel` into an exportable module and export it using `torch.export`,
    ensuring the exported model is compatible with `ExecuTorch`.

    Args:
        model (`PreTrainedModel`): The pretrained model to be exported.
        example_input_ids (`Optional[torch.Tensor]`): Example input token id used by `torch.export`.
        example_cache_position (`Optional[torch.Tensor]`): Example current cache position used by `torch.export`.
        dynamic_shapes(`Optional[dict]`): Dynamic shapes used by `torch.export`.
        strict(`Optional[bool]`): Flag to instruct `torch.export` to use `torchdynamo`.

    Returns:
        Exported program (`torch.export.ExportedProgram`): The exported program generated via `torch.export`.
    """

    import torch.export._trace

    with torch.no_grad():
        # TODO: The default inputs only work for text models. We need to add support for vision/audio models.
        example_input_ids = (
            example_input_ids
            if example_input_ids is not None
            else torch.tensor([[1]], dtype=torch.long, device=model.device)
        )
        example_cache_position = (
            example_cache_position
            if example_cache_position is not None
            else torch.tensor([0], dtype=torch.long, device=model.device)
        )

        if is_torch_greater_or_equal("2.6.0"):
            exported_program = torch.export.export(
                TorchExportableModuleWithStaticCache(model),
                args=(),
                kwargs={"input_ids": example_input_ids, "cache_position": example_cache_position},
                dynamic_shapes=dynamic_shapes,
                strict=strict if strict is not None else True,
            )
        else:
            if dynamic_shapes is not None:
                logging.warning(
                    "Dynamic shapes spec will be ignored by convert_and_export_with_cache for torch < 2.6.0."
                )
            if strict is not None:
                logging.warning("The strict flag will be ignored by convert_and_export_with_cache for torch < 2.6.0.")
            # We have to keep this path for BC.
            #
            # Due to issue https://github.com/pytorch/pytorch/issues/128394, we need to switch to use an internal
            # export API and pre_dispatch=False. Switch to use the public API once the issue is included in 2.5 release.
            exported_program = torch.export._trace._export(
                TorchExportableModuleWithStaticCache(model),
                args=(),
                kwargs={"input_ids": example_input_ids, "cache_position": example_cache_position},
                pre_dispatch=False,
                strict=True,
            )
        return exported_program


def convert_and_export_with_cache(*args, **kwargs):
    requires_backends(convert_and_export_with_cache, ["torch"])

