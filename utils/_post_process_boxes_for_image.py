
def _post_process_boxes_for_image(
    boxes: "torch.Tensor",
    scores: "torch.Tensor",
    labels: "torch.Tensor",
    image_num_classes: int,
    image_size: tuple[int, int],
    threshold: float,
    nms_threshold: float,
    max_num_det: int | None = None,
) -> tuple["torch.Tensor", "torch.Tensor", "torch.Tensor"]:
    """
    Filter predicted results using given thresholds and NMS.

    Args:
        boxes (`torch.Tensor`):
            A Tensor of predicted class-specific or class-agnostic boxes for the image.
            Shape (num_queries, max_num_classes_in_batch * 4) if doing class-specific regression,
            or (num_queries, 4) if doing class-agnostic regression.
        scores (`torch.Tensor` of shape (num_queries, max_num_classes_in_batch + 1)):
            A Tensor of predicted class scores for the image.
        labels (`torch.Tensor` of shape (num_queries * (max_num_classes_in_batch + 1),)):
            A Tensor of predicted labels for the image.
        image_num_classes (`int`):
            The number of classes queried for detection on the image.
        image_size (`tuple[int, int]`):
            A tuple of (height, width) for the image.
        threshold (`float`):
            Only return detections with a confidence score exceeding this threshold.
        nms_threshold (`float`):
            The threshold to use for box non-maximum suppression. Value in [0, 1].
        max_num_det (`int`, *optional*):
            The maximum number of detections to return. Default is None.

    Returns:
        Tuple: A tuple with the following:
            "boxes" (Tensor): A tensor of shape (num_filtered_objects, 4), containing the predicted boxes in (x1, y1, x2, y2) format.
            "scores" (Tensor): A tensor of shape (num_filtered_objects,), containing the predicted confidence scores for each detection.
            "labels" (Tensor): A tensor of ids, where each id is the predicted class id for the corresponding detection
    """

    # Filter by max number of detections
    proposal_num = len(boxes) if max_num_det is None else max_num_det
    scores_per_image, topk_indices = scores.flatten(0, 1).topk(proposal_num, sorted=False)
    labels_per_image = labels[topk_indices]
    boxes_per_image = boxes.view(-1, 1, 4).repeat(1, scores.shape[1], 1).view(-1, 4)
    boxes_per_image = boxes_per_image[topk_indices]

    # Convert and scale boxes to original image size
    boxes_per_image = center_to_corners_format(boxes_per_image)
    boxes_per_image = boxes_per_image * torch.tensor(image_size[::-1]).repeat(2).to(boxes_per_image.device)

    # Filtering by confidence score
    filter_mask = scores_per_image > threshold  # R x K
    score_keep = filter_mask.nonzero(as_tuple=False).view(-1)
    boxes_per_image = boxes_per_image[score_keep]
    scores_per_image = scores_per_image[score_keep]
    labels_per_image = labels_per_image[score_keep]

    # Ensure we did not overflow to non existing classes
    filter_classes_mask = labels_per_image < image_num_classes
    classes_keep = filter_classes_mask.nonzero(as_tuple=False).view(-1)
    boxes_per_image = boxes_per_image[classes_keep]
    scores_per_image = scores_per_image[classes_keep]
    labels_per_image = labels_per_image[classes_keep]

    # NMS
    keep = batched_nms(boxes_per_image, scores_per_image, labels_per_image, nms_threshold)
    boxes_per_image = boxes_per_image[keep]
    scores_per_image = scores_per_image[keep]
    labels_per_image = labels_per_image[keep]

    # Clip to image size
    boxes_per_image = clip_boxes(boxes_per_image, image_size)

    return boxes_per_image, scores_per_image, labels_per_image

