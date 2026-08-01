
def RfDetrForSegmentationLoss(
    logits,
    labels,
    device,
    pred_boxes,
    pred_masks,
    config,
    outputs_class=None,
    outputs_coord=None,
    outputs_masks=None,
    enc_outputs_class=None,
    enc_outputs_coord=None,
    enc_outputs_masks=None,
    **kwargs,
):
    # First: create the matcher
    matcher = RfDetrHungarianMatcher(
        class_cost=config.class_cost,
        bbox_cost=config.bbox_cost,
        giou_cost=config.giou_cost,
        mask_point_sample_ratio=config.mask_point_sample_ratio,
        cost_mask_class_cost=config.mask_class_loss_coefficient,
        cost_mask_dice_cost=config.mask_dice_loss_coefficient,
    )
    # Second: create the criterion
    losses = ["labels", "boxes", "cardinality", "masks"]
    criterion = RfDetrImageLoss(
        matcher=matcher,
        num_classes=config.num_labels,
        focal_alpha=config.focal_alpha,
        losses=losses,
        group_detr=config.group_detr,
        mask_point_sample_ratio=config.mask_point_sample_ratio,
    )
    criterion.to(device)
    # Third: compute the losses, based on outputs and labels
    outputs_loss = {}
    auxiliary_outputs = None
    outputs_loss["logits"] = logits
    outputs_loss["pred_boxes"] = pred_boxes
    outputs_loss["pred_masks"] = pred_masks
    outputs_loss["enc_outputs"] = {
        "logits": enc_outputs_class,
        "pred_boxes": enc_outputs_coord,
        "pred_masks": enc_outputs_masks,
    }
    if config.auxiliary_loss:
        auxiliary_outputs = _set_aux_loss(outputs_class, outputs_coord, outputs_masks)
        outputs_loss["auxiliary_outputs"] = auxiliary_outputs

    loss_dict = criterion(outputs_loss, labels)
    # Fourth: compute total loss, as a weighted sum of the various losses
    weight_dict = {"loss_ce": config.class_loss_coefficient, "loss_bbox": config.bbox_loss_coefficient}
    weight_dict["loss_giou"] = config.giou_loss_coefficient
    weight_dict["loss_mask_ce"] = config.mask_class_loss_coefficient
    weight_dict["loss_mask_dice"] = config.mask_dice_loss_coefficient
    if config.auxiliary_loss:
        aux_weight_dict = {}
        for i in range(config.decoder_layers - 1):
            aux_weight_dict.update({k + f"_{i}": v for k, v in weight_dict.items()})
        aux_weight_dict.update({k + "_enc": v for k, v in weight_dict.items()})
        weight_dict.update(aux_weight_dict)
    loss = sum(loss_dict[k] * weight_dict[k] for k in loss_dict if k in weight_dict)
    return loss, loss_dict, auxiliary_outputs

