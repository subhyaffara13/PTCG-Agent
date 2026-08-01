
def image_boxes(
    tag, tensor_image, tensor_boxes, rescale=1, dataformats="CHW", labels=None
):
    """Output a `Summary` protocol buffer with images."""
    tensor_image = make_np(tensor_image)
    tensor_image = convert_to_HWC(tensor_image, dataformats)
    tensor_boxes = make_np(tensor_boxes)
    tensor_image = tensor_image.astype(np.float32) * _calc_scale_factor(tensor_image)
    image = make_image(
        tensor_image.clip(0, 255).astype(np.uint8),
        rescale=rescale,
        rois=tensor_boxes,
        labels=labels,
    )
    return Summary(value=[Summary.Value(tag=tag, image=image)])

