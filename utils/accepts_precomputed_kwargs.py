
def accepts_precomputed_kwargs(modality: str):
    """
    Decorator for `get_<modality>_features` methods that:
      - strips the modality prefix from incoming kwargs whose stripped name isn't an existing
        parameter (e.g. `image_cu_seqlens` → `cu_seqlens`, forwarded via `**kwargs`);
      - drops kwargs prefixed with another known modality (e.g. `video_*` passed to an
        image method), so an outer `forward()` can blindly forward `**kwargs` to each
        modality method without leaking the wrong tensors into the wrong encoder;
      - leaves everything else untouched (including kwargs that match a named parameter).

    Used so multimodal models can accept arbitrary precomputed tensors (`image_cu_seqlens`,
    `video_position_ids`, …) without enumerating each one in every signature.

    NOTE: Apply this decorator **only once per modality**, on the innermost base model's
    `get_<modality>_features` (i.e. on `Model.get_image_features`, not on the outer
    `ForConditionalGeneration.get_image_features` wrapper). Stacking it at multiple layers
    causes premature prefix-stripping: the outer layer rewrites `image_foo` → `foo` based
    on its own (narrower) signature, hiding kwargs that the inner method declares as named
    parameters. Outer wrappers should just forward `**kwargs` through.

    TODO: these modality-prefixed kwargs (`image_cu_seqlens`, `video_position_ids`, …) are
    currently power-feature-only — they have no visible declaration in any public signature,
    so users have to discover them from helper functions or docs. We should find a way to
    surface them properly (e.g. in `TransformersKwargs`, in a dedicated `MultimodalKwargs`
    typed dict, or returned grouped from the processor as `BatchFeature.images_data={...}`)
    so the supported set is discoverable in one place.
    """
    prefix = f"{modality}_"
    other_prefixes = tuple(f"{m}_" for m in _KNOWN_MODALITIES if m != modality)

    def decorator(func):
        existing_params = set(inspect.signature(func).parameters)

        @wraps(func)
        def wrapper(*args, **kwargs):
            translated = {}
            for k, v in kwargs.items():
                if k.startswith(other_prefixes):
                    continue
                if k.startswith(prefix) and k not in existing_params:
                    translated[k.removeprefix(prefix)] = v
                else:
                    translated[k] = v
            return func(*args, **translated)

        return wrapper

    return decorator

