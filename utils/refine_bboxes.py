
def refine_bboxes(reference_points, deltas):
    reference_points = reference_points.to(deltas.device)
    new_reference_points_cxcy = deltas[..., :2] * reference_points[..., 2:] + reference_points[..., :2]
    new_reference_points_wh = deltas[..., 2:].exp() * reference_points[..., 2:]
    new_reference_points = torch.cat((new_reference_points_cxcy, new_reference_points_wh), -1)
    return new_reference_points


def refine_bboxes(reference_points, deltas):
    reference_points = reference_points.to(deltas.device)
    new_reference_points_cxcy = deltas[..., :2] * reference_points[..., 2:] + reference_points[..., :2]
    new_reference_points_wh = deltas[..., 2:].exp() * reference_points[..., 2:]
    new_reference_points = torch.cat((new_reference_points_cxcy, new_reference_points_wh), -1)
    return new_reference_points


def refine_bboxes(reference_points, deltas):
    reference_points = reference_points.to(deltas.device)
    new_reference_points_cxcy = deltas[..., :2] * reference_points[..., 2:] + reference_points[..., :2]
    new_reference_points_wh = deltas[..., 2:].exp() * reference_points[..., 2:]
    new_reference_points = torch.cat((new_reference_points_cxcy, new_reference_points_wh), -1)
    return new_reference_points

