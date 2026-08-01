
def cudagraph_annotation_context(
    cudagraphs: BoxedBool,
) -> contextlib.AbstractContextManager[None]:
    # When an annotation force-enables cudagraphs but the global config has them
    # off, patch config.triton.cudagraphs for the duration of compilation,
    # so existing codepaths that access config.triton.cudagraphs work
    if cudagraphs.value and not config.triton.cudagraphs:
        return config.patch({"triton.cudagraphs": True})
    return contextlib.nullcontext()

