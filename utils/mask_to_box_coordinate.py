
def mask_to_box_coordinate(mask, dtype):
    mask = mask.bool()

    height, width = mask.shape[-2:]

    y_coords, x_coords = torch.meshgrid(
        torch.arange(height, device=mask.device), torch.arange(width, device=mask.device), indexing="ij"
    )
    x_coords = x_coords.to(dtype)
    y_coords = y_coords.to(dtype)

    x_coords_masked = x_coords * mask
    x_max = x_coords_masked.flatten(start_dim=-2).max(dim=-1).values + 1
    x_min = (
        torch.where(mask, x_coords_masked, torch.tensor(torch.finfo(dtype).max))
        .flatten(start_dim=-2)
        .min(dim=-1)
        .values
    )

    y_coords_masked = y_coords * mask
    y_max = y_coords_masked.flatten(start_dim=-2).max(dim=-1).values + 1
    y_min = (
        torch.where(mask, y_coords_masked, torch.tensor(torch.finfo(dtype).max))
        .flatten(start_dim=-2)
        .min(dim=-1)
        .values
    )

    unnormalized_bbox = torch.stack([x_min, y_min, x_max, y_max], dim=-1)

    is_mask_non_empty = torch.any(mask, dim=(-2, -1)).unsqueeze(-1)
    unnormalized_bbox = unnormalized_bbox * is_mask_non_empty

    norm_tensor = torch.tensor([width, height, width, height], device=mask.device, dtype=dtype)
    normalized_bbox_xyxy = unnormalized_bbox / norm_tensor

    x_min_norm, y_min_norm, x_max_norm, y_max_norm = normalized_bbox_xyxy.unbind(dim=-1)

    center_x = (x_min_norm + x_max_norm) / 2
    center_y = (y_min_norm + y_max_norm) / 2
    box_width = x_max_norm - x_min_norm
    box_height = y_max_norm - y_min_norm

    return torch.stack([center_x, center_y, box_width, box_height], dim=-1)


def mask_to_box_coordinate(mask, dtype):
    mask = mask.bool()

    height, width = mask.shape[-2:]

    y_coords, x_coords = torch.meshgrid(
        torch.arange(height, device=mask.device), torch.arange(width, device=mask.device), indexing="ij"
    )
    x_coords = x_coords.to(dtype)
    y_coords = y_coords.to(dtype)

    x_coords_masked = x_coords * mask
    x_max = x_coords_masked.flatten(start_dim=-2).max(dim=-1).values + 1
    x_min = (
        torch.where(mask, x_coords_masked, torch.tensor(torch.finfo(dtype).max))
        .flatten(start_dim=-2)
        .min(dim=-1)
        .values
    )

    y_coords_masked = y_coords * mask
    y_max = y_coords_masked.flatten(start_dim=-2).max(dim=-1).values + 1
    y_min = (
        torch.where(mask, y_coords_masked, torch.tensor(torch.finfo(dtype).max))
        .flatten(start_dim=-2)
        .min(dim=-1)
        .values
    )

    unnormalized_bbox = torch.stack([x_min, y_min, x_max, y_max], dim=-1)

    is_mask_non_empty = torch.any(mask, dim=(-2, -1)).unsqueeze(-1)
    unnormalized_bbox = unnormalized_bbox * is_mask_non_empty

    norm_tensor = torch.tensor([width, height, width, height], device=mask.device, dtype=dtype)
    normalized_bbox_xyxy = unnormalized_bbox / norm_tensor

    x_min_norm, y_min_norm, x_max_norm, y_max_norm = normalized_bbox_xyxy.unbind(dim=-1)

    center_x = (x_min_norm + x_max_norm) / 2
    center_y = (y_min_norm + y_max_norm) / 2
    box_width = x_max_norm - x_min_norm
    box_height = y_max_norm - y_min_norm

    return torch.stack([center_x, center_y, box_width, box_height], dim=-1)

