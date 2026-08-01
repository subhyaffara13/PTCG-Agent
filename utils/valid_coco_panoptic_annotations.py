
def valid_coco_panoptic_annotations(annotations: Iterable[dict[str, list | tuple]]) -> bool:
    return all(is_valid_annotation_coco_panoptic(ann) for ann in annotations)

