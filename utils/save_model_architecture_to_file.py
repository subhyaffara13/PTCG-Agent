
def save_model_architecture_to_file(model: Any, output_dir: str):
    with open(f"{output_dir}/model_architecture.txt", "w+") as f:
        if isinstance(model, PreTrainedModel):
            print(model, file=f)
        elif is_torch_available() and (
            isinstance(model, (torch.nn.Module, PushToHubMixin)) and hasattr(model, "base_model")
        ):
            print(model, file=f)

