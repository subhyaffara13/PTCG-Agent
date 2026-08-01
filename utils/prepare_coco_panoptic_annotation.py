
def prepare_coco_panoptic_annotation(
    image: torch.Tensor,
    target: dict,
    masks_path: str | pathlib.Path,
    return_masks: bool = True,
    input_data_format: ChannelDimension | str = None,
) -> dict:
    """
    Prepare a coco panoptic annotation for CONDITIONAL_DETR.
    """
    image_height, image_width = get_image_size(image, channel_dim=input_data_format)
    annotation_path = pathlib.Path(masks_path) / target["file_name"]

    new_target = {}
    new_target["image_id"] = torch.as_tensor(
        [target["image_id"] if "image_id" in target else target["id"]], dtype=torch.int64, device=image.device
    )
    new_target["size"] = torch.as_tensor([image_height, image_width], dtype=torch.int64, device=image.device)
    new_target["orig_size"] = torch.as_tensor([image_height, image_width], dtype=torch.int64, device=image.device)

    if "segments_info" in target:
        masks = read_image(annotation_path).permute(1, 2, 0).to(dtype=torch.int32, device=image.device)
        masks = rgb_to_id(masks)

        ids = torch.as_tensor([segment_info["id"] for segment_info in target["segments_info"]], device=image.device)
        masks = masks == ids[:, None, None]
        masks = masks.to(torch.bool)
        if return_masks:
            new_target["masks"] = masks
        new_target["boxes"] = masks_to_boxes(masks)
        new_target["class_labels"] = torch.as_tensor(
            [segment_info["category_id"] for segment_info in target["segments_info"]],
            dtype=torch.int64,
            device=image.device,
        )
        new_target["iscrowd"] = torch.as_tensor(
            [segment_info["iscrowd"] for segment_info in target["segments_info"]],
            dtype=torch.int64,
            device=image.device,
        )
        new_target["area"] = torch.as_tensor(
            [segment_info["area"] for segment_info in target["segments_info"]],
            dtype=torch.float32,
            device=image.device,
        )

    return new_target


def prepare_coco_panoptic_annotation(
    image: np.ndarray,
    target: dict,
    masks_path: str | pathlib.Path,
    return_masks: bool = True,
    input_data_format: ChannelDimension | str = None,
) -> dict:
    """
    Prepare a coco panoptic annotation for CONDITIONAL_DETR.
    """
    image_height, image_width = get_image_size(image, channel_dim=input_data_format)
    annotation_path = pathlib.Path(masks_path) / target["file_name"]

    new_target = {}
    new_target["image_id"] = np.asarray([target["image_id"] if "image_id" in target else target["id"]], dtype=np.int64)
    new_target["size"] = np.asarray([image_height, image_width], dtype=np.int64)
    new_target["orig_size"] = np.asarray([image_height, image_width], dtype=np.int64)

    if "segments_info" in target:
        masks = np.asarray(PIL.Image.open(annotation_path), dtype=np.uint32)
        masks = rgb_to_id(masks)

        ids = np.array([segment_info["id"] for segment_info in target["segments_info"]])
        masks = masks == ids[:, None, None]
        masks = masks.astype(np.uint8)
        if return_masks:
            new_target["masks"] = masks
        new_target["boxes"] = masks_to_boxes(masks)
        new_target["class_labels"] = np.array(
            [segment_info["category_id"] for segment_info in target["segments_info"]], dtype=np.int64
        )
        new_target["iscrowd"] = np.asarray(
            [segment_info["iscrowd"] for segment_info in target["segments_info"]], dtype=np.int64
        )
        new_target["area"] = np.asarray(
            [segment_info["area"] for segment_info in target["segments_info"]], dtype=np.float32
        )

    return new_target


def prepare_coco_panoptic_annotation(
    image: torch.Tensor,
    target: dict,
    masks_path: str | pathlib.Path,
    return_masks: bool = True,
    input_data_format: ChannelDimension | str = None,
) -> dict:
    """
    Prepare a coco panoptic annotation for DEFORMABLE_DETR.
    """
    image_height, image_width = get_image_size(image, channel_dim=input_data_format)
    annotation_path = pathlib.Path(masks_path) / target["file_name"]

    new_target = {}
    new_target["image_id"] = torch.as_tensor(
        [target["image_id"] if "image_id" in target else target["id"]], dtype=torch.int64, device=image.device
    )
    new_target["size"] = torch.as_tensor([image_height, image_width], dtype=torch.int64, device=image.device)
    new_target["orig_size"] = torch.as_tensor([image_height, image_width], dtype=torch.int64, device=image.device)

    if "segments_info" in target:
        masks = read_image(annotation_path).permute(1, 2, 0).to(dtype=torch.int32, device=image.device)
        masks = rgb_to_id(masks)

        ids = torch.as_tensor([segment_info["id"] for segment_info in target["segments_info"]], device=image.device)
        masks = masks == ids[:, None, None]
        masks = masks.to(torch.bool)
        if return_masks:
            new_target["masks"] = masks
        new_target["boxes"] = masks_to_boxes(masks)
        new_target["class_labels"] = torch.as_tensor(
            [segment_info["category_id"] for segment_info in target["segments_info"]],
            dtype=torch.int64,
            device=image.device,
        )
        new_target["iscrowd"] = torch.as_tensor(
            [segment_info["iscrowd"] for segment_info in target["segments_info"]],
            dtype=torch.int64,
            device=image.device,
        )
        new_target["area"] = torch.as_tensor(
            [segment_info["area"] for segment_info in target["segments_info"]],
            dtype=torch.float32,
            device=image.device,
        )

    return new_target


def prepare_coco_panoptic_annotation(
    image: np.ndarray,
    target: dict,
    masks_path: str | pathlib.Path,
    return_masks: bool = True,
    input_data_format: ChannelDimension | str = None,
) -> dict:
    """
    Prepare a coco panoptic annotation for DEFORMABLE_DETR.
    """
    image_height, image_width = get_image_size(image, channel_dim=input_data_format)
    annotation_path = pathlib.Path(masks_path) / target["file_name"]

    new_target = {}
    new_target["image_id"] = np.asarray([target["image_id"] if "image_id" in target else target["id"]], dtype=np.int64)
    new_target["size"] = np.asarray([image_height, image_width], dtype=np.int64)
    new_target["orig_size"] = np.asarray([image_height, image_width], dtype=np.int64)

    if "segments_info" in target:
        masks = np.asarray(PIL.Image.open(annotation_path), dtype=np.uint32)
        masks = rgb_to_id(masks)

        ids = np.array([segment_info["id"] for segment_info in target["segments_info"]])
        masks = masks == ids[:, None, None]
        masks = masks.astype(np.uint8)
        if return_masks:
            new_target["masks"] = masks
        new_target["boxes"] = masks_to_boxes(masks)
        new_target["class_labels"] = np.array(
            [segment_info["category_id"] for segment_info in target["segments_info"]], dtype=np.int64
        )
        new_target["iscrowd"] = np.asarray(
            [segment_info["iscrowd"] for segment_info in target["segments_info"]], dtype=np.int64
        )
        new_target["area"] = np.asarray(
            [segment_info["area"] for segment_info in target["segments_info"]], dtype=np.float32
        )

    return new_target


def prepare_coco_panoptic_annotation(
    image: torch.Tensor,
    target: dict,
    masks_path: str | pathlib.Path,
    return_masks: bool = True,
    input_data_format: ChannelDimension | str = None,
) -> dict:
    """
    Prepare a coco panoptic annotation for DETR.
    """
    image_height, image_width = get_image_size(image, channel_dim=input_data_format)
    annotation_path = pathlib.Path(masks_path) / target["file_name"]

    new_target = {}
    new_target["image_id"] = torch.as_tensor(
        [target["image_id"] if "image_id" in target else target["id"]], dtype=torch.int64, device=image.device
    )
    new_target["size"] = torch.as_tensor([image_height, image_width], dtype=torch.int64, device=image.device)
    new_target["orig_size"] = torch.as_tensor([image_height, image_width], dtype=torch.int64, device=image.device)

    if "segments_info" in target:
        masks = read_image(annotation_path).permute(1, 2, 0).to(dtype=torch.int32, device=image.device)
        masks = rgb_to_id(masks)

        ids = torch.as_tensor([segment_info["id"] for segment_info in target["segments_info"]], device=image.device)
        masks = masks == ids[:, None, None]
        masks = masks.to(torch.bool)
        if return_masks:
            new_target["masks"] = masks
        new_target["boxes"] = masks_to_boxes(masks)
        new_target["class_labels"] = torch.as_tensor(
            [segment_info["category_id"] for segment_info in target["segments_info"]],
            dtype=torch.int64,
            device=image.device,
        )
        new_target["iscrowd"] = torch.as_tensor(
            [segment_info["iscrowd"] for segment_info in target["segments_info"]],
            dtype=torch.int64,
            device=image.device,
        )
        new_target["area"] = torch.as_tensor(
            [segment_info["area"] for segment_info in target["segments_info"]],
            dtype=torch.float32,
            device=image.device,
        )

    return new_target


def prepare_coco_panoptic_annotation(
    image: np.ndarray,
    target: dict,
    masks_path: str | pathlib.Path,
    return_masks: bool = True,
    input_data_format: ChannelDimension | str = None,
) -> dict:
    """
    Prepare a coco panoptic annotation for DETR.
    """
    image_height, image_width = get_image_size(image, channel_dim=input_data_format)
    annotation_path = pathlib.Path(masks_path) / target["file_name"]

    new_target = {}
    new_target["image_id"] = np.asarray([target["image_id"] if "image_id" in target else target["id"]], dtype=np.int64)
    new_target["size"] = np.asarray([image_height, image_width], dtype=np.int64)
    new_target["orig_size"] = np.asarray([image_height, image_width], dtype=np.int64)

    if "segments_info" in target:
        masks = np.asarray(PIL.Image.open(annotation_path), dtype=np.uint32)
        masks = rgb_to_id(masks)

        ids = np.array([segment_info["id"] for segment_info in target["segments_info"]])
        masks = masks == ids[:, None, None]
        masks = masks.astype(np.uint8)
        if return_masks:
            new_target["masks"] = masks
        new_target["boxes"] = masks_to_boxes(masks)
        new_target["class_labels"] = np.array(
            [segment_info["category_id"] for segment_info in target["segments_info"]], dtype=np.int64
        )
        new_target["iscrowd"] = np.asarray(
            [segment_info["iscrowd"] for segment_info in target["segments_info"]], dtype=np.int64
        )
        new_target["area"] = np.asarray(
            [segment_info["area"] for segment_info in target["segments_info"]], dtype=np.float32
        )

    return new_target


def prepare_coco_panoptic_annotation(
    image: torch.Tensor,
    target: dict,
    masks_path: str | pathlib.Path,
    return_masks: bool = True,
    input_data_format: ChannelDimension | str = None,
) -> dict:
    """
    Prepare a coco panoptic annotation for GROUNDING_DINO.
    """
    image_height, image_width = get_image_size(image, channel_dim=input_data_format)
    annotation_path = pathlib.Path(masks_path) / target["file_name"]

    new_target = {}
    new_target["image_id"] = torch.as_tensor(
        [target["image_id"] if "image_id" in target else target["id"]], dtype=torch.int64, device=image.device
    )
    new_target["size"] = torch.as_tensor([image_height, image_width], dtype=torch.int64, device=image.device)
    new_target["orig_size"] = torch.as_tensor([image_height, image_width], dtype=torch.int64, device=image.device)

    if "segments_info" in target:
        masks = read_image(annotation_path).permute(1, 2, 0).to(dtype=torch.int32, device=image.device)
        masks = rgb_to_id(masks)

        ids = torch.as_tensor([segment_info["id"] for segment_info in target["segments_info"]], device=image.device)
        masks = masks == ids[:, None, None]
        masks = masks.to(torch.bool)
        if return_masks:
            new_target["masks"] = masks
        new_target["boxes"] = masks_to_boxes(masks)
        new_target["class_labels"] = torch.as_tensor(
            [segment_info["category_id"] for segment_info in target["segments_info"]],
            dtype=torch.int64,
            device=image.device,
        )
        new_target["iscrowd"] = torch.as_tensor(
            [segment_info["iscrowd"] for segment_info in target["segments_info"]],
            dtype=torch.int64,
            device=image.device,
        )
        new_target["area"] = torch.as_tensor(
            [segment_info["area"] for segment_info in target["segments_info"]],
            dtype=torch.float32,
            device=image.device,
        )

    return new_target


def prepare_coco_panoptic_annotation(
    image: np.ndarray,
    target: dict,
    masks_path: str | pathlib.Path,
    return_masks: bool = True,
    input_data_format: ChannelDimension | str = None,
) -> dict:
    """
    Prepare a coco panoptic annotation for GROUNDING_DINO.
    """
    image_height, image_width = get_image_size(image, channel_dim=input_data_format)
    annotation_path = pathlib.Path(masks_path) / target["file_name"]

    new_target = {}
    new_target["image_id"] = np.asarray([target["image_id"] if "image_id" in target else target["id"]], dtype=np.int64)
    new_target["size"] = np.asarray([image_height, image_width], dtype=np.int64)
    new_target["orig_size"] = np.asarray([image_height, image_width], dtype=np.int64)

    if "segments_info" in target:
        masks = np.asarray(PIL.Image.open(annotation_path), dtype=np.uint32)
        masks = rgb_to_id(masks)

        ids = np.array([segment_info["id"] for segment_info in target["segments_info"]])
        masks = masks == ids[:, None, None]
        masks = masks.astype(np.uint8)
        if return_masks:
            new_target["masks"] = masks
        new_target["boxes"] = masks_to_boxes(masks)
        new_target["class_labels"] = np.array(
            [segment_info["category_id"] for segment_info in target["segments_info"]], dtype=np.int64
        )
        new_target["iscrowd"] = np.asarray(
            [segment_info["iscrowd"] for segment_info in target["segments_info"]], dtype=np.int64
        )
        new_target["area"] = np.asarray(
            [segment_info["area"] for segment_info in target["segments_info"]], dtype=np.float32
        )

    return new_target


def prepare_coco_panoptic_annotation(
    image: np.ndarray,
    target: dict,
    masks_path: str | pathlib.Path,
    return_masks: bool = True,
    input_data_format: ChannelDimension | str = None,
) -> dict:
    """
    Prepare a coco panoptic annotation for YOLOS.
    """
    image_height, image_width = get_image_size(image, channel_dim=input_data_format)
    annotation_path = pathlib.Path(masks_path) / target["file_name"]

    new_target = {}
    new_target["image_id"] = np.asarray([target["image_id"] if "image_id" in target else target["id"]], dtype=np.int64)
    new_target["size"] = np.asarray([image_height, image_width], dtype=np.int64)
    new_target["orig_size"] = np.asarray([image_height, image_width], dtype=np.int64)

    if "segments_info" in target:
        masks = np.asarray(PIL.Image.open(annotation_path), dtype=np.uint32)
        masks = rgb_to_id(masks)

        ids = np.array([segment_info["id"] for segment_info in target["segments_info"]])
        masks = masks == ids[:, None, None]
        masks = masks.astype(np.uint8)
        if return_masks:
            new_target["masks"] = masks
        new_target["boxes"] = masks_to_boxes(masks)
        new_target["class_labels"] = np.array(
            [segment_info["category_id"] for segment_info in target["segments_info"]], dtype=np.int64
        )
        new_target["iscrowd"] = np.asarray(
            [segment_info["iscrowd"] for segment_info in target["segments_info"]], dtype=np.int64
        )
        new_target["area"] = np.asarray(
            [segment_info["area"] for segment_info in target["segments_info"]], dtype=np.float32
        )

    return new_target


def prepare_coco_panoptic_annotation(
    image: torch.Tensor,
    target: dict,
    masks_path: str | pathlib.Path,
    return_masks: bool = True,
    input_data_format: ChannelDimension | str = None,
) -> dict:
    """
    Prepare a coco panoptic annotation for YOLOS.
    """
    image_height, image_width = get_image_size(image, channel_dim=input_data_format)
    annotation_path = pathlib.Path(masks_path) / target["file_name"]

    new_target = {}
    new_target["image_id"] = torch.as_tensor(
        [target["image_id"] if "image_id" in target else target["id"]], dtype=torch.int64, device=image.device
    )
    new_target["size"] = torch.as_tensor([image_height, image_width], dtype=torch.int64, device=image.device)
    new_target["orig_size"] = torch.as_tensor([image_height, image_width], dtype=torch.int64, device=image.device)

    if "segments_info" in target:
        masks = read_image(annotation_path).permute(1, 2, 0).to(dtype=torch.int32, device=image.device)
        masks = rgb_to_id(masks)

        ids = torch.as_tensor([segment_info["id"] for segment_info in target["segments_info"]], device=image.device)
        masks = masks == ids[:, None, None]
        masks = masks.to(torch.bool)
        if return_masks:
            new_target["masks"] = masks
        new_target["boxes"] = masks_to_boxes(masks)
        new_target["class_labels"] = torch.as_tensor(
            [segment_info["category_id"] for segment_info in target["segments_info"]],
            dtype=torch.int64,
            device=image.device,
        )
        new_target["iscrowd"] = torch.as_tensor(
            [segment_info["iscrowd"] for segment_info in target["segments_info"]],
            dtype=torch.int64,
            device=image.device,
        )
        new_target["area"] = torch.as_tensor(
            [segment_info["area"] for segment_info in target["segments_info"]],
            dtype=torch.float32,
            device=image.device,
        )

    return new_target

