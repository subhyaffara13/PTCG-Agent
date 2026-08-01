
def sample_points_using_uncertainty(
    logits: Tensor, num_points: int, oversample_ratio: int, importance_sample_ratio: float
) -> Tensor:
    """
    This function is meant for sampling points in [0, 1] * [0, 1] coordinate space based on their uncertainty. The
    uncertainty is calculated for each point using the passed `uncertainty function` that takes points logit
    prediction as input.

    Args:
        logits (`float`):
            Logit predictions for P points.
        uncertainty_function:
            A function that takes logit predictions for P points and returns their uncertainties.
        num_points (`int`):
            The number of points P to sample.
        oversample_ratio (`int`):
            Oversampling parameter.
        importance_sample_ratio (`float`):
            Ratio of points that are sampled via importance sampling.

    Returns:
        point_coordinates (`torch.Tensor`):
            Coordinates for P sampled points.
    """

    num_boxes = logits.shape[0]
    num_points_sampled = int(num_points * oversample_ratio)

    # Get random point coordinates
    point_coordinates = torch.rand(num_boxes, num_points_sampled, 2, device=logits.device)
    # Get sampled prediction value for the point coordinates
    point_logits = sample_point(logits, point_coordinates, align_corners=False)
    # Calculate the uncertainties based on the sampled prediction values of the points
    point_uncertainties = -(torch.abs(point_logits))

    num_uncertain_points = int(importance_sample_ratio * num_points)
    num_random_points = num_points - num_uncertain_points

    idx = torch.topk(point_uncertainties[:, 0, :], k=num_uncertain_points, dim=1)[1]
    point_coordinates = torch.gather(point_coordinates, 1, idx.unsqueeze(-1).expand(-1, -1, 2))

    if num_random_points > 0:
        point_coordinates = torch.cat(
            [point_coordinates, torch.rand(num_boxes, num_random_points, 2, device=logits.device)],
            dim=1,
        )
    return point_coordinates

