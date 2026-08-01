
def _set_aux_loss(outputs_class, outputs_coord):
    return [{"logits": a, "pred_boxes": b} for a, b in zip(outputs_class, outputs_coord)]


def _set_aux_loss(outputs_class, outputs_coord):
    return [{"logits": a, "pred_boxes": b} for a, b in zip(outputs_class[:-1], outputs_coord[:-1])]


def _set_aux_loss(outputs_class, outputs_coord, outputs_masks):
    # Difference with LwDetrImageLoss: we extend auxiliary outputs for masks
    return [
        {"logits": a, "pred_boxes": b, "pred_masks": c}
        for a, b, c in zip(outputs_class[:-1], outputs_coord[:-1], outputs_masks[:-1])
    ]


def _set_aux_loss(outputs_class, outputs_coord):
    return [{"logits": a, "pred_boxes": b} for a, b in zip(outputs_class, outputs_coord)]

