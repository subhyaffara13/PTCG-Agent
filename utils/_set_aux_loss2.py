
def _set_aux_loss2(
    outputs_class, outputs_coord, outputs_corners, outputs_ref, teacher_corners=None, teacher_logits=None
):
    return [
        {
            "logits": a,
            "pred_boxes": b,
            "pred_corners": c,
            "ref_points": d,
            "teacher_corners": teacher_corners,
            "teacher_logits": teacher_logits,
        }
        for a, b, c, d in zip(outputs_class, outputs_coord, outputs_corners, outputs_ref)
    ]

