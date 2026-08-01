
def valid_coco_detection_annotations(annotations: Iterable[dict[str, list | tuple]]) -> bool:
    return all(is_valid_annotation_coco_detection(ann) for ann in annotations)

