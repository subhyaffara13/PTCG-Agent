import os
from typing import List, Tuple, Union

def load_model(
    model: torch.nn.Module,
    filename: Union[str, os.PathLike],
    strict: bool = True,
    device: Union[str, int] = "cpu",
    *,
    backend: str = "mmap",
) -> Tuple[List[str], List[str]]:
    """
    Loads a given filename onto a torch model.
    This method exists specifically to avoid tensor sharing issues which are
    not allowed in `safetensors`. [More information on tensor sharing](../torch_shared_tensors)

    Args:
        model (`torch.nn.Module`):
            The model to load onto.
        filename (`str`, or `os.PathLike`):
            The filename location to load the file from.
        strict (`bool`, *optional*, defaults to True):
            Whether to fail if you're missing keys or having unexpected ones.
            When false, the function simply returns missing and unexpected names.
        device (`Union[str, int]`, *optional*, defaults to `cpu`):
            The device where the tensors need to be located after load.
            available options are all regular torch device locations.
        backend (`str`, *optional*, defaults to `"mmap"`):
            Storage backend used to serve tensor bytes. `"mmap"` (default)
            and `"pread"` uses `pread(2)` to read tensor bytes.

    Returns:
        `(missing, unexpected): (List[str], List[str])`
            `missing` are names in the model which were not modified during loading
            `unexpected` are names that are on the file, but weren't used during
            the load.
    """
    state_dict = load_file(filename, device=device, backend=backend)
    model_state_dict = model.state_dict()
    to_removes = _remove_duplicate_names(
        model_state_dict, preferred_names=state_dict.keys()
    )
    missing, unexpected = model.load_state_dict(state_dict, strict=False)
    missing = set(missing)
    for to_remove_group in to_removes.values():
        for to_remove in to_remove_group:
            if to_remove not in missing:
                unexpected.append(to_remove)
            else:
                missing.remove(to_remove)
    if strict and (missing or unexpected):
        missing_keys = ", ".join([f'"{k}"' for k in sorted(missing)])
        unexpected_keys = ", ".join([f'"{k}"' for k in sorted(unexpected)])
        error = f"Error(s) in loading state_dict for {model.__class__.__name__}:"
        if missing:
            error += f"\n    Missing key(s) in state_dict: {missing_keys}"
        if unexpected:
            error += f"\n    Unexpected key(s) in state_dict: {unexpected_keys}"
        raise RuntimeError(error)
    return missing, unexpected


def load_model(
    model,
    config: AutoConfig,
    model_classes: tuple[type, ...] | None = None,
    task: str | None = None,
    **model_kwargs,
):
    """
    Load a model.

    If `model` is instantiated, this function will just return it. Otherwise `model` is
    actually a checkpoint name and this method will try to instantiate it using `model_classes`. Since we don't want to
    instantiate the model twice, this model is returned for use by the pipeline.

    Args:
        model (`str`, or [`PreTrainedModel`]):
            If `str`, a checkpoint name. The model to load.
        config ([`AutoConfig`]):
            The config associated with the model to help using the correct class
        model_classes (`tuple[type]`, *optional*):
            A tuple of model classes.
        task (`str`):
            The task defining which pipeline will be returned.
        model_kwargs:
            Additional dictionary of keyword arguments passed along to the model's `from_pretrained(...,
            **model_kwargs)` function.

    Returns:
        The model.
    """
    if not is_torch_available():
        raise RuntimeError("PyTorch should be installed. Please follow the instructions at https://pytorch.org/.")

    if isinstance(model, str):
        model_kwargs["_from_pipeline"] = task
        class_tuple = model_classes if model_classes is not None else ()
        if config.architectures:
            classes = []
            for architecture in config.architectures:
                transformers_module = importlib.import_module("transformers")
                _class = getattr(transformers_module, architecture, None)
                if _class is not None:
                    classes.append(_class)
            class_tuple = class_tuple + tuple(classes)

        if len(class_tuple) == 0:
            raise ValueError(f"Pipeline cannot infer suitable model classes from {model}")

        all_traceback = {}
        for model_class in class_tuple:
            kwargs = model_kwargs.copy()

            try:
                model = model_class.from_pretrained(model, **kwargs)
                # Stop loading on the first successful load.
                break
            except (OSError, ValueError, TypeError, RuntimeError):
                # `from_pretrained` may raise a `TypeError` or `RuntimeError` when the requested `dtype`
                # is not supported on the execution device (e.g. bf16 on a consumer GPU). We capture those so
                # we can transparently retry the load in float32 before surfacing an error to the user.
                fallback_tried = False
                if "dtype" in kwargs:
                    import torch

                    fallback_tried = True
                    fp32_kwargs = kwargs.copy()
                    fp32_kwargs["dtype"] = torch.float32

                    try:
                        model = model_class.from_pretrained(model, **fp32_kwargs)
                        logger.warning(
                            "Falling back to torch.float32 because loading with the original dtype failed on the"
                            " target device."
                        )
                        break
                    except Exception:
                        # If it still fails, capture the traceback and continue to the next class.
                        all_traceback[model_class.__name__] = traceback.format_exc()
                        continue

                # If no fallback was attempted or it also failed, record the original traceback.
                if not fallback_tried:
                    all_traceback[model_class.__name__] = traceback.format_exc()
                continue

        if isinstance(model, str):
            error = ""
            for class_name, trace in all_traceback.items():
                error += f"while loading with {class_name}, an error is thrown:\n{trace}\n"
            raise ValueError(
                f"Could not load model {model} with any of the following classes: {class_tuple}. See the original errors:\n\n{error}\n"
            )

    return model


def load_model():
  net = hk.without_apply_rng(hk.transform(net_fn))
  params = pickle.load(
      open(os.path.join(FLAGS.params_path, "params-snapshot.pkl"), "rb"))
  return net, params

