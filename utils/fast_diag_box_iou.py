
def fast_diag_box_iou(boxes1, boxes2):
    box1_xy = boxes1[:, 2:]
    box1_XY = boxes1[:, :2]
    box2_xy = boxes2[:, 2:]
    box2_XY = boxes2[:, :2]
    area1 = (box1_xy - box1_XY).prod(-1)
    area2 = (box2_xy - box2_XY).prod(-1)

    lt = torch.max(box1_XY, box2_XY)
    rb = torch.min(box1_xy, box2_xy)

    inter = (rb - lt).clamp(min=0).prod(-1)
    union = area1 + area2 - inter
    iou = inter / union
    return iou

