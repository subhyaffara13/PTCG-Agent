
def _post_process_for_mask_generation(rle_masks, iou_scores, mask_boxes, amg_crops_nms_thresh=0.7):
    """
    Perform NMS (Non Maximum Suppression) on the outputs.

    Args:
            rle_masks (`torch.Tensor`):
                binary masks in the RLE format
            iou_scores (`torch.Tensor` of shape (nb_masks, 1)):
                iou_scores predicted by the model
            mask_boxes (`torch.Tensor`):
                The bounding boxes corresponding to segmentation masks
            amg_crops_nms_thresh (`float`, *optional*, defaults to 0.7):
                NMS threshold.
    """
    if not is_torch_available():
        raise ImportError("PyTorch is required for post_process_for_mask_generation")

    import torch
    from torchvision.ops.boxes import batched_nms

    keep_by_nms = batched_nms(
        boxes=mask_boxes.float(),
        scores=iou_scores,
        idxs=torch.zeros(mask_boxes.shape[0]),
        iou_threshold=amg_crops_nms_thresh,
    )

    iou_scores = iou_scores[keep_by_nms]
    rle_masks = [rle_masks[i] for i in keep_by_nms]
    mask_boxes = mask_boxes[keep_by_nms]
    masks = [_rle_to_mask(rle) for rle in rle_masks]

    return masks, iou_scores, rle_masks, mask_boxes


def _post_process_for_mask_generation(rle_masks, iou_scores, mask_boxes, amg_crops_nms_thresh=0.7):
    """
    Perform NMS (Non Maximum Suppression) on the outputs.

    Args:
            rle_masks (`torch.Tensor`):
                binary masks in the RLE format
            iou_scores (`torch.Tensor` of shape (nb_masks, 1)):
                iou_scores predicted by the model
            mask_boxes (`torch.Tensor`):
                The bounding boxes corresponding to segmentation masks
            amg_crops_nms_thresh (`float`, *optional*, defaults to 0.7):
                NMS threshold.
    """
    keep_by_nms = batched_nms(
        boxes=mask_boxes.float(),
        scores=iou_scores,
        idxs=torch.zeros(mask_boxes.shape[0]),
        iou_threshold=amg_crops_nms_thresh,
    )

    iou_scores = iou_scores[keep_by_nms]
    rle_masks = [rle_masks[i] for i in keep_by_nms]
    mask_boxes = mask_boxes[keep_by_nms]
    masks = [_rle_to_mask(rle) for rle in rle_masks]

    return masks, iou_scores, rle_masks, mask_boxes


def _post_process_for_mask_generation(rle_masks, iou_scores, mask_boxes, amg_crops_nms_thresh=0.7):
    """
    Perform NMS (Non Maximum Suppression) on the outputs.

    Args:
            rle_masks (`torch.Tensor`):
                binary masks in the RLE format
            iou_scores (`torch.Tensor` of shape (nb_masks, 1)):
                iou_scores predicted by the model
            mask_boxes (`torch.Tensor`):
                The bounding boxes corresponding to segmentation masks
            amg_crops_nms_thresh (`float`, *optional*, defaults to 0.7):
                NMS threshold.
    """
    keep_by_nms = batched_nms(
        boxes=mask_boxes.float(),
        scores=iou_scores,
        idxs=torch.zeros(mask_boxes.shape[0]),
        iou_threshold=amg_crops_nms_thresh,
    )

    iou_scores = iou_scores[keep_by_nms]
    rle_masks = [rle_masks[i] for i in keep_by_nms]
    mask_boxes = mask_boxes[keep_by_nms]
    masks = [_rle_to_mask(rle) for rle in rle_masks]

    return masks, iou_scores, rle_masks, mask_boxes


def _post_process_for_mask_generation(rle_masks, iou_scores, mask_boxes, amg_crops_nms_thresh=0.7):
    """
    Perform NMS (Non Maximum Suppression) on the outputs.

    Args:
            rle_masks (`torch.Tensor`):
                binary masks in the RLE format
            iou_scores (`torch.Tensor` of shape (nb_masks, 1)):
                iou_scores predicted by the model
            mask_boxes (`torch.Tensor`):
                The bounding boxes corresponding to segmentation masks
            amg_crops_nms_thresh (`float`, *optional*, defaults to 0.7):
                NMS threshold.
    """
    keep_by_nms = batched_nms(
        boxes=mask_boxes.float(),
        scores=iou_scores,
        idxs=torch.zeros(mask_boxes.shape[0]),
        iou_threshold=amg_crops_nms_thresh,
    )

    iou_scores = iou_scores[keep_by_nms]
    rle_masks = [rle_masks[i] for i in keep_by_nms]
    mask_boxes = mask_boxes[keep_by_nms]
    masks = [_rle_to_mask(rle) for rle in rle_masks]

    return masks, iou_scores, rle_masks, mask_boxes

