
def numpy_nms(boxes: Tensor, scores: Tensor, iou_threshold: Number) -> Tensor:
    # Adapted from Ross Girshick's fast-rcnn implementation at
    # https://github.com/rbgirshick/fast-rcnn/blob/master/lib/utils/nms.py
    if boxes.device != scores.device:
        raise AssertionError(f"boxes.device={boxes.device} != scores.device={scores.device}")
    device = boxes.device

    boxes = to_numpy(boxes)
    scores = to_numpy(scores)

    N = boxes.shape[0]
    if boxes.shape != (N, 4):
        raise AssertionError(f"boxes.shape must be (N, 4), got {boxes.shape}")
    if scores.shape != (N,):
        raise AssertionError(f"scores.shape must be (N,), got {scores.shape}")

    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter)

        inds = np.where(ovr <= iou_threshold)[0]
        order = order[inds + 1]

    result = torch.tensor(np.stack(keep), device=device)
    # Needed for data-dependent condition :(
    if result.size(0) < 2:
        raise AssertionError(f"result.size(0) must be >= 2, got {result.size(0)}")
    return result

