
def _load_backend_class(base_class_name, backend, is_legacy_fast=False):
    """
    Load image processor class for a given backend. Uses the mapping from
    IMAGE_PROCESSOR_MAPPING when base_class_name is found in its values (so config
    overrides and custom backends are respected). Falls back to base+Pil convention
    for remote code / unknown processors.
    """
    mapping = _find_mapping_for_image_processor(base_class_name)
    if mapping is None:
        mapping = {
            "torchvision": base_class_name,
            "pil": base_class_name + "Pil",
        }
    processor_class = _load_class_with_fallback(mapping, backend)

    # For legacy Fast classes, try the original Fast class name as last resort
    if processor_class is None and is_legacy_fast:
        processor_class = get_image_processor_class_from_name(base_class_name + "Fast")

    return processor_class

