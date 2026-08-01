
def convert_segmentation_map_to_binary_masks(
    segmentation_map: np.ndarray,
    instance_id_to_semantic_id: dict[int, int] | None = None,
    ignore_index: int | None = None,
):
    if ignore_index is not None:
        segmentation_map = np.where(segmentation_map == 0, ignore_index, segmentation_map - 1)

    # Get unique ids (class or instance ids based on input)
    all_labels = np.unique(segmentation_map)

    # Drop background label if applicable
    if ignore_index is not None:
        all_labels = all_labels[all_labels != ignore_index]

    # Generate a binary mask for each object instance
    binary_masks = [(segmentation_map == i) for i in all_labels]

    # Stack the binary masks
    if binary_masks:
        binary_masks = np.stack(binary_masks, axis=0)
    else:
        binary_masks = np.zeros((0, *segmentation_map.shape))

    # Convert instance ids to class ids
    if instance_id_to_semantic_id is not None:
        labels = np.zeros(all_labels.shape[0])

        for label in all_labels:
            class_id = instance_id_to_semantic_id[label + 1 if ignore_index is not None else label]
            labels[all_labels == label] = class_id - 1 if ignore_index is not None else class_id
    else:
        labels = all_labels

    return binary_masks.astype(np.float32), labels.astype(np.int64)


def convert_segmentation_map_to_binary_masks(
    segmentation_map: np.ndarray,
    instance_id_to_semantic_id: dict[int, int] | None = None,
    ignore_index: int | None = None,
    do_reduce_labels: bool = False,
):
    """Convert segmentation map to binary masks using NumPy operations."""
    if do_reduce_labels and ignore_index is None:
        raise ValueError("If `do_reduce_labels` is True, `ignore_index` must be provided.")

    if do_reduce_labels:
        segmentation_map = np.where(segmentation_map == 0, ignore_index, segmentation_map - 1)

    all_labels = np.unique(segmentation_map)

    if ignore_index is not None:
        all_labels = all_labels[all_labels != ignore_index]

    binary_masks = [(segmentation_map == i) for i in all_labels]
    if binary_masks:
        binary_masks = np.stack(binary_masks, axis=0)
    else:
        binary_masks = np.zeros((0, *segmentation_map.shape), dtype=np.float32)

    # Convert instance ids to class ids
    if instance_id_to_semantic_id is not None:
        labels = np.zeros(all_labels.shape[0], dtype=np.int64)

        for i, label in enumerate(all_labels):
            class_id = instance_id_to_semantic_id[(int(label) + 1 if do_reduce_labels else int(label))]
            labels[i] = class_id - 1 if do_reduce_labels else class_id
    else:
        labels = all_labels.astype(np.int64)
    return binary_masks.astype(np.float32), labels


def convert_segmentation_map_to_binary_masks(
    segmentation_map: np.ndarray,
    instance_id_to_semantic_id: dict[int, int] | None = None,
    ignore_index: int | None = None,
    do_reduce_labels: bool = False,
):
    """Convert segmentation map to binary masks using NumPy operations."""
    if do_reduce_labels and ignore_index is None:
        raise ValueError("If `do_reduce_labels` is True, `ignore_index` must be provided.")

    if do_reduce_labels:
        segmentation_map = np.where(segmentation_map == 0, ignore_index, segmentation_map - 1)

    all_labels = np.unique(segmentation_map)

    if ignore_index is not None:
        all_labels = all_labels[all_labels != ignore_index]

    binary_masks = [(segmentation_map == i) for i in all_labels]
    if binary_masks:
        binary_masks = np.stack(binary_masks, axis=0)
    else:
        binary_masks = np.zeros((0, *segmentation_map.shape), dtype=np.float32)

    # Convert instance ids to class ids
    if instance_id_to_semantic_id is not None:
        labels = np.zeros(all_labels.shape[0], dtype=np.int64)

        for i, label in enumerate(all_labels):
            class_id = instance_id_to_semantic_id[(int(label) + 1 if do_reduce_labels else int(label))]
            labels[i] = class_id - 1 if do_reduce_labels else class_id
    else:
        labels = all_labels.astype(np.int64)
    return binary_masks.astype(np.float32), labels

