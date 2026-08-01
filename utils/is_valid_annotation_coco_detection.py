
def is_valid_annotation_coco_detection(annotation: dict[str, list | tuple]) -> bool:
    if (
        isinstance(annotation, dict)
        and "image_id" in annotation
        and "annotations" in annotation
        and isinstance(annotation["annotations"], (list, tuple))
        and (
            # an image can have no annotations
            len(annotation["annotations"]) == 0 or isinstance(annotation["annotations"][0], dict)
        )
    ):
        return True
    return False

