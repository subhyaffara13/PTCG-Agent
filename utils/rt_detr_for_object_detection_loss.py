
def RTDetrForObjectDetectionLoss(
    logits,
    labels,
    device,
    pred_boxes,
    config,
    outputs_class=None,
    outputs_coord=None,
    enc_topk_logits=None,
    enc_topk_bboxes=None,
    denoising_meta_values=None,
    **kwargs,
):
    criterion = RTDetrLoss(config)
    criterion.to(device)
    # Second: compute the losses, based on outputs and labels
    outputs_loss = {}
    outputs_loss["logits"] = logits
    outputs_loss["pred_boxes"] = pred_boxes
    auxiliary_outputs = None
    if config.auxiliary_loss:
        if denoising_meta_values is not None:
            dn_out_coord, outputs_coord = torch.split(outputs_coord, denoising_meta_values["dn_num_split"], dim=2)
            dn_out_class, outputs_class = torch.split(outputs_class, denoising_meta_values["dn_num_split"], dim=2)

        auxiliary_outputs = _set_aux_loss(outputs_class[:, :-1].transpose(0, 1), outputs_coord[:, :-1].transpose(0, 1))
        outputs_loss["auxiliary_outputs"] = auxiliary_outputs
        outputs_loss["auxiliary_outputs"].extend(_set_aux_loss([enc_topk_logits], [enc_topk_bboxes]))
        if denoising_meta_values is not None:
            outputs_loss["dn_auxiliary_outputs"] = _set_aux_loss(
                dn_out_class.transpose(0, 1), dn_out_coord.transpose(0, 1)
            )
            outputs_loss["denoising_meta_values"] = denoising_meta_values

    loss_dict = criterion(outputs_loss, labels)

    loss = sum(loss_dict.values())
    return loss, loss_dict, auxiliary_outputs

