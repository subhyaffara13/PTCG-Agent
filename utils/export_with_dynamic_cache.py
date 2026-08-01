
def export_with_dynamic_cache(
    model: PreTrainedModel,
    example_input_ids: torch.Tensor | None = None,
    example_attention_mask: torch.Tensor | None = None,
):
    """
    Export a model with DynamicCache using `torch.export`, ensuring the exported model is compatible with `ExecuTorch`.

    Args:
        model (`PreTrainedModel`): The pretrained model to be exported.
        example_input_ids (`Optional[torch.Tensor]`): Example input token id used by `torch.export`.
        example_attention_mask (`Optional[torch.Tensor]`): Example attention mask used by `torch.export`.

    Returns:
        Exported program (`torch.export.ExportedProgram`): The exported program generated via `torch.export`.
    """

    register_dynamic_cache_export_support()

    with torch.no_grad():
        exported_program = torch.export.export(
            model,
            (),
            {
                "input_ids": example_input_ids,
                "attention_mask": example_attention_mask,
                "past_key_values": DynamicCache(config=model.config),
                "use_cache": True,
            },
            strict=False,
        )
        return exported_program

