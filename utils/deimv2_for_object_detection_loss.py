
def Deimv2ForObjectDetectionLoss(
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
    predicted_corners=None,
    initial_reference_points=None,
    **kwargs,
):
    criterion = Deimv2Loss(config)
    criterion.to(device)

    outputs_loss = {"logits": logits, "pred_boxes": pred_boxes.clamp(min=0, max=1)}
    auxiliary_outputs = None

    if config.auxiliary_loss:
        if denoising_meta_values is not None:
            dn_out_coord, normal_out_coord = torch.split(
                outputs_coord.clamp(min=0, max=1), denoising_meta_values["dn_num_split"], dim=2
            )
            dn_out_class, normal_out_class = torch.split(outputs_class, denoising_meta_values["dn_num_split"], dim=2)
            # https://github.com/Intellindust-AI-Lab/DEIMv2/blob/main/engine/deim/deim_decoder.py#L562-L571
            # The original splits denoising queries in the decoder; here it happens in the loss since the decoder returns unsplit tensors.
            _, normal_logits = torch.split(logits, denoising_meta_values["dn_num_split"], dim=1)
            _, normal_pred_boxes = torch.split(pred_boxes, denoising_meta_values["dn_num_split"], dim=1)
            dn_out_corners, out_corners = torch.split(predicted_corners, denoising_meta_values["dn_num_split"], dim=2)
            dn_out_refs, out_refs = torch.split(initial_reference_points, denoising_meta_values["dn_num_split"], dim=2)

            outputs_loss["logits"] = normal_logits
            outputs_loss["pred_boxes"] = normal_pred_boxes.clamp(min=0, max=1)
        else:
            normal_out_coord = outputs_coord.clamp(min=0, max=1)
            normal_out_class = outputs_class
            out_corners = predicted_corners
            out_refs = initial_reference_points

        auxiliary_outputs = _set_aux_loss2(
            normal_out_class[:, :-1].transpose(0, 1),
            normal_out_coord[:, :-1].transpose(0, 1),
            out_corners[:, :-1].transpose(0, 1),
            out_refs[:, :-1].transpose(0, 1),
            out_corners[:, -1],
            normal_out_class[:, -1],
        )

        outputs_loss["auxiliary_outputs"] = auxiliary_outputs
        outputs_loss["auxiliary_outputs"].extend(
            _set_aux_loss([enc_topk_logits], [enc_topk_bboxes.clamp(min=0, max=1)])
        )

        if denoising_meta_values is not None:
            dn_auxiliary_outputs = _set_aux_loss2(
                dn_out_class.transpose(0, 1),
                dn_out_coord.transpose(0, 1),
                dn_out_corners.transpose(0, 1),
                dn_out_refs.transpose(0, 1),
                dn_out_corners[:, -1],
                dn_out_class[:, -1],
            )
            outputs_loss["dn_auxiliary_outputs"] = dn_auxiliary_outputs
            outputs_loss["denoising_meta_values"] = denoising_meta_values

    loss_dict = criterion(outputs_loss, labels)

    loss = sum(loss_dict.values())
    return loss, loss_dict, auxiliary_outputs

