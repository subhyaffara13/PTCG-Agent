
def masks_to_boxes(masks: torch.Tensor) -> torch.Tensor:
    """
    Compute the bounding boxes around the provided panoptic segmentation masks.

    Args:
        masks: masks in format `[number_masks, height, width]` where N is the number of masks

    Returns:
        boxes: bounding boxes in format `[number_masks, 4]` in xyxy format
    """
    if masks.numel() == 0:
        return torch.zeros((0, 4), device=masks.device)

    h, w = masks.shape[-2:]
    y = torch.arange(0, h, dtype=torch.float32, device=masks.device)
    x = torch.arange(0, w, dtype=torch.float32, device=masks.device)
    # see https://github.com/pytorch/pytorch/issues/50276
    y, x = torch.meshgrid(y, x, indexing="ij")

    x_mask = masks * torch.unsqueeze(x, 0)
    x_max = x_mask.view(x_mask.shape[0], -1).max(-1)[0]
    x_min = (
        torch.where(masks, x.unsqueeze(0), torch.tensor(1e8, device=masks.device)).view(masks.shape[0], -1).min(-1)[0]
    )

    y_mask = masks * torch.unsqueeze(y, 0)
    y_max = y_mask.view(y_mask.shape[0], -1).max(-1)[0]
    y_min = (
        torch.where(masks, y.unsqueeze(0), torch.tensor(1e8, device=masks.device)).view(masks.shape[0], -1).min(-1)[0]
    )

    return torch.stack([x_min, y_min, x_max, y_max], 1)


def masks_to_boxes(masks: np.ndarray) -> np.ndarray:
    """
    Compute the bounding boxes around the provided panoptic segmentation masks.

    Args:
        masks: masks in format `[number_masks, height, width]` where N is the number of masks

    Returns:
        boxes: bounding boxes in format `[number_masks, 4]` in xyxy format
    """
    if masks.size == 0:
        return np.zeros((0, 4))

    h, w = masks.shape[-2:]
    y = np.arange(0, h, dtype=np.float32)
    x = np.arange(0, w, dtype=np.float32)
    # see https://github.com/pytorch/pytorch/issues/50276
    y, x = np.meshgrid(y, x, indexing="ij")

    x_mask = masks * np.expand_dims(x, axis=0)
    x_max = x_mask.reshape(x_mask.shape[0], -1).max(-1)
    x = np.ma.array(x_mask, mask=~(np.array(masks, dtype=bool)))
    x_min = x.filled(fill_value=1e8)
    x_min = x_min.reshape(x_min.shape[0], -1).min(-1)

    y_mask = masks * np.expand_dims(y, axis=0)
    y_max = y_mask.reshape(x_mask.shape[0], -1).max(-1)
    y = np.ma.array(y_mask, mask=~(np.array(masks, dtype=bool)))
    y_min = y.filled(fill_value=1e8)
    y_min = y_min.reshape(y_min.shape[0], -1).min(-1)

    return np.stack([x_min, y_min, x_max, y_max], 1)


def masks_to_boxes(masks: torch.Tensor) -> torch.Tensor:
    """
    Compute the bounding boxes around the provided panoptic segmentation masks.

    Args:
        masks: masks in format `[number_masks, height, width]` where N is the number of masks

    Returns:
        boxes: bounding boxes in format `[number_masks, 4]` in xyxy format
    """
    if masks.numel() == 0:
        return torch.zeros((0, 4), device=masks.device)

    h, w = masks.shape[-2:]
    y = torch.arange(0, h, dtype=torch.float32, device=masks.device)
    x = torch.arange(0, w, dtype=torch.float32, device=masks.device)
    # see https://github.com/pytorch/pytorch/issues/50276
    y, x = torch.meshgrid(y, x, indexing="ij")

    x_mask = masks * torch.unsqueeze(x, 0)
    x_max = x_mask.view(x_mask.shape[0], -1).max(-1)[0]
    x_min = (
        torch.where(masks, x.unsqueeze(0), torch.tensor(1e8, device=masks.device)).view(masks.shape[0], -1).min(-1)[0]
    )

    y_mask = masks * torch.unsqueeze(y, 0)
    y_max = y_mask.view(y_mask.shape[0], -1).max(-1)[0]
    y_min = (
        torch.where(masks, y.unsqueeze(0), torch.tensor(1e8, device=masks.device)).view(masks.shape[0], -1).min(-1)[0]
    )

    return torch.stack([x_min, y_min, x_max, y_max], 1)


def masks_to_boxes(masks: np.ndarray) -> np.ndarray:
    """
    Compute the bounding boxes around the provided panoptic segmentation masks.

    Args:
        masks: masks in format `[number_masks, height, width]` where N is the number of masks

    Returns:
        boxes: bounding boxes in format `[number_masks, 4]` in xyxy format
    """
    if masks.size == 0:
        return np.zeros((0, 4))

    h, w = masks.shape[-2:]
    y = np.arange(0, h, dtype=np.float32)
    x = np.arange(0, w, dtype=np.float32)
    # see https://github.com/pytorch/pytorch/issues/50276
    y, x = np.meshgrid(y, x, indexing="ij")

    x_mask = masks * np.expand_dims(x, axis=0)
    x_max = x_mask.reshape(x_mask.shape[0], -1).max(-1)
    x = np.ma.array(x_mask, mask=~(np.array(masks, dtype=bool)))
    x_min = x.filled(fill_value=1e8)
    x_min = x_min.reshape(x_min.shape[0], -1).min(-1)

    y_mask = masks * np.expand_dims(y, axis=0)
    y_max = y_mask.reshape(x_mask.shape[0], -1).max(-1)
    y = np.ma.array(y_mask, mask=~(np.array(masks, dtype=bool)))
    y_min = y.filled(fill_value=1e8)
    y_min = y_min.reshape(y_min.shape[0], -1).min(-1)

    return np.stack([x_min, y_min, x_max, y_max], 1)


def masks_to_boxes(masks: torch.Tensor) -> torch.Tensor:
    """
    Compute the bounding boxes around the provided panoptic segmentation masks.

    Args:
        masks: masks in format `[number_masks, height, width]` where N is the number of masks

    Returns:
        boxes: bounding boxes in format `[number_masks, 4]` in xyxy format
    """
    if masks.numel() == 0:
        return torch.zeros((0, 4), device=masks.device)

    h, w = masks.shape[-2:]
    y = torch.arange(0, h, dtype=torch.float32, device=masks.device)
    x = torch.arange(0, w, dtype=torch.float32, device=masks.device)
    # see https://github.com/pytorch/pytorch/issues/50276
    y, x = torch.meshgrid(y, x, indexing="ij")

    x_mask = masks * torch.unsqueeze(x, 0)
    x_max = x_mask.view(x_mask.shape[0], -1).max(-1)[0]
    x_min = (
        torch.where(masks, x.unsqueeze(0), torch.tensor(1e8, device=masks.device)).view(masks.shape[0], -1).min(-1)[0]
    )

    y_mask = masks * torch.unsqueeze(y, 0)
    y_max = y_mask.view(y_mask.shape[0], -1).max(-1)[0]
    y_min = (
        torch.where(masks, y.unsqueeze(0), torch.tensor(1e8, device=masks.device)).view(masks.shape[0], -1).min(-1)[0]
    )

    return torch.stack([x_min, y_min, x_max, y_max], 1)


def masks_to_boxes(masks: np.ndarray) -> np.ndarray:
    """
    Compute the bounding boxes around the provided panoptic segmentation masks.

    Args:
        masks: masks in format `[number_masks, height, width]` where N is the number of masks

    Returns:
        boxes: bounding boxes in format `[number_masks, 4]` in xyxy format
    """
    if masks.size == 0:
        return np.zeros((0, 4))

    h, w = masks.shape[-2:]
    y = np.arange(0, h, dtype=np.float32)
    x = np.arange(0, w, dtype=np.float32)
    # see https://github.com/pytorch/pytorch/issues/50276
    y, x = np.meshgrid(y, x, indexing="ij")

    x_mask = masks * np.expand_dims(x, axis=0)
    x_max = x_mask.reshape(x_mask.shape[0], -1).max(-1)
    x = np.ma.array(x_mask, mask=~(np.array(masks, dtype=bool)))
    x_min = x.filled(fill_value=1e8)
    x_min = x_min.reshape(x_min.shape[0], -1).min(-1)

    y_mask = masks * np.expand_dims(y, axis=0)
    y_max = y_mask.reshape(x_mask.shape[0], -1).max(-1)
    y = np.ma.array(y_mask, mask=~(np.array(masks, dtype=bool)))
    y_min = y.filled(fill_value=1e8)
    y_min = y_min.reshape(y_min.shape[0], -1).min(-1)

    return np.stack([x_min, y_min, x_max, y_max], 1)


def masks_to_boxes(masks: torch.Tensor) -> torch.Tensor:
    """
    Compute the bounding boxes around the provided panoptic segmentation masks.

    Args:
        masks: masks in format `[number_masks, height, width]` where N is the number of masks

    Returns:
        boxes: bounding boxes in format `[number_masks, 4]` in xyxy format
    """
    if masks.numel() == 0:
        return torch.zeros((0, 4), device=masks.device)

    h, w = masks.shape[-2:]
    y = torch.arange(0, h, dtype=torch.float32, device=masks.device)
    x = torch.arange(0, w, dtype=torch.float32, device=masks.device)
    # see https://github.com/pytorch/pytorch/issues/50276
    y, x = torch.meshgrid(y, x, indexing="ij")

    x_mask = masks * torch.unsqueeze(x, 0)
    x_max = x_mask.view(x_mask.shape[0], -1).max(-1)[0]
    x_min = (
        torch.where(masks, x.unsqueeze(0), torch.tensor(1e8, device=masks.device)).view(masks.shape[0], -1).min(-1)[0]
    )

    y_mask = masks * torch.unsqueeze(y, 0)
    y_max = y_mask.view(y_mask.shape[0], -1).max(-1)[0]
    y_min = (
        torch.where(masks, y.unsqueeze(0), torch.tensor(1e8, device=masks.device)).view(masks.shape[0], -1).min(-1)[0]
    )

    return torch.stack([x_min, y_min, x_max, y_max], 1)


def masks_to_boxes(masks: np.ndarray) -> np.ndarray:
    """
    Compute the bounding boxes around the provided panoptic segmentation masks.

    Args:
        masks: masks in format `[number_masks, height, width]` where N is the number of masks

    Returns:
        boxes: bounding boxes in format `[number_masks, 4]` in xyxy format
    """
    if masks.size == 0:
        return np.zeros((0, 4))

    h, w = masks.shape[-2:]
    y = np.arange(0, h, dtype=np.float32)
    x = np.arange(0, w, dtype=np.float32)
    # see https://github.com/pytorch/pytorch/issues/50276
    y, x = np.meshgrid(y, x, indexing="ij")

    x_mask = masks * np.expand_dims(x, axis=0)
    x_max = x_mask.reshape(x_mask.shape[0], -1).max(-1)
    x = np.ma.array(x_mask, mask=~(np.array(masks, dtype=bool)))
    x_min = x.filled(fill_value=1e8)
    x_min = x_min.reshape(x_min.shape[0], -1).min(-1)

    y_mask = masks * np.expand_dims(y, axis=0)
    y_max = y_mask.reshape(x_mask.shape[0], -1).max(-1)
    y = np.ma.array(y_mask, mask=~(np.array(masks, dtype=bool)))
    y_min = y.filled(fill_value=1e8)
    y_min = y_min.reshape(y_min.shape[0], -1).min(-1)

    return np.stack([x_min, y_min, x_max, y_max], 1)


def masks_to_boxes(masks: np.ndarray) -> np.ndarray:
    """
    Compute the bounding boxes around the provided panoptic segmentation masks.

    Args:
        masks: masks in format `[number_masks, height, width]` where N is the number of masks

    Returns:
        boxes: bounding boxes in format `[number_masks, 4]` in xyxy format
    """
    if masks.size == 0:
        return np.zeros((0, 4))

    h, w = masks.shape[-2:]
    y = np.arange(0, h, dtype=np.float32)
    x = np.arange(0, w, dtype=np.float32)
    # see https://github.com/pytorch/pytorch/issues/50276
    y, x = np.meshgrid(y, x, indexing="ij")

    x_mask = masks * np.expand_dims(x, axis=0)
    x_max = x_mask.reshape(x_mask.shape[0], -1).max(-1)
    x = np.ma.array(x_mask, mask=~(np.array(masks, dtype=bool)))
    x_min = x.filled(fill_value=1e8)
    x_min = x_min.reshape(x_min.shape[0], -1).min(-1)

    y_mask = masks * np.expand_dims(y, axis=0)
    y_max = y_mask.reshape(x_mask.shape[0], -1).max(-1)
    y = np.ma.array(y_mask, mask=~(np.array(masks, dtype=bool)))
    y_min = y.filled(fill_value=1e8)
    y_min = y_min.reshape(y_min.shape[0], -1).min(-1)

    return np.stack([x_min, y_min, x_max, y_max], 1)


def masks_to_boxes(masks: torch.Tensor) -> torch.Tensor:
    """
    Compute the bounding boxes around the provided panoptic segmentation masks.

    Args:
        masks: masks in format `[number_masks, height, width]` where N is the number of masks

    Returns:
        boxes: bounding boxes in format `[number_masks, 4]` in xyxy format
    """
    if masks.numel() == 0:
        return torch.zeros((0, 4), device=masks.device)

    h, w = masks.shape[-2:]
    y = torch.arange(0, h, dtype=torch.float32, device=masks.device)
    x = torch.arange(0, w, dtype=torch.float32, device=masks.device)
    # see https://github.com/pytorch/pytorch/issues/50276
    y, x = torch.meshgrid(y, x, indexing="ij")

    x_mask = masks * torch.unsqueeze(x, 0)
    x_max = x_mask.view(x_mask.shape[0], -1).max(-1)[0]
    x_min = (
        torch.where(masks, x.unsqueeze(0), torch.tensor(1e8, device=masks.device)).view(masks.shape[0], -1).min(-1)[0]
    )

    y_mask = masks * torch.unsqueeze(y, 0)
    y_max = y_mask.view(y_mask.shape[0], -1).max(-1)[0]
    y_min = (
        torch.where(masks, y.unsqueeze(0), torch.tensor(1e8, device=masks.device)).view(masks.shape[0], -1).min(-1)[0]
    )

    return torch.stack([x_min, y_min, x_max, y_max], 1)

