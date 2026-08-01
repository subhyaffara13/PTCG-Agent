
def model_addition_debugger_context(
    model,
    debug_path: str | None = None,
    do_prune_layers: bool = True,
    use_repr: bool = True,
):
    """
    # Model addition debugger - context manager for model adders
    This context manager is a power user tool intended for model adders.

    It tracks all forward calls within a model forward and logs a slice of each input and output on a nested JSON file.
    If `use_repr=True` (the default), the JSON file will record a `repr()`-ized version of the tensors as a list of
    strings. If `use_repr=False`, the full tensors will be stored in separate SafeTensors files and the JSON file will
    provide a relative path to that file.

    To note, this context manager enforces `torch.no_grad()`.

    ## Usage

    add the context manager to a model to debug

    ```python
    import torch

    from PIL import Image
    from transformers import LlavaProcessor, LlavaForConditionalGeneration, model_addition_debugger_context

    torch.random.manual_seed(673)

    # load pretrained model and processor
    model_id = "llava-hf/llava-1.5-7b-hf"
    processor = LlavaProcessor.from_pretrained(model_id)
    model = LlavaForConditionalGeneration.from_pretrained(model_id)

    # create random image input
    random_image = Image.fromarray(torch.randint(0, 256, (224, 224, 3), dtype=torch.uint8).numpy())

    # prompt
    prompt = "<image>Describe this image."

    # process inputs
    inputs = processor(text=prompt, images=random_image, return_tensors="pt")

    # call forward method (not .generate!)
    with model_addition_debugger_context(model, debug_path="Your_debug_path", do_prune_layers=False):
        output = model.forward(**inputs)
    ```

    """
    orig_forwards = {m: m.forward for _, m in model.named_modules()}
    orig_forwards[model] = model.forward
    _attach_debugger_logic(model, debug_path, do_prune_layers, use_repr)
    try:
        yield model
    finally:
        for module_instance, forward_method in orig_forwards.items():
            module_instance.forward = forward_method


def model_addition_debugger_context(*args, **kwargs):
    requires_backends(model_addition_debugger_context, ["torch"])

