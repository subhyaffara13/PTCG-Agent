
def process_controlnet_arguments(args):
    """
    Process control net arguments, and returns a list of control images and a tensor of control net scales.
    """
    assert isinstance(args.controlnet_type, list)
    assert isinstance(args.controlnet_scale, list)
    assert isinstance(args.controlnet_image, list)

    if len(args.controlnet_image) != len(args.controlnet_type):
        raise ValueError(
            f"Numbers of controlnet_image {len(args.controlnet_image)} should be equal to number of controlnet_type {len(args.controlnet_type)}."
        )

    if len(args.controlnet_type) == 0:
        return None, None

    if args.version not in ["1.5", "xl-1.0", "xl-turbo", "sd-turbo"]:
        raise ValueError("This demo only supports ControlNet in Stable Diffusion 1.5, XL or Turbo.")

    is_xl = "xl" in args.version
    if is_xl and len(args.controlnet_type) > 1:
        raise ValueError("This demo only support one ControlNet for Stable Diffusion XL or Turbo.")

    if len(args.controlnet_scale) == 0:
        args.controlnet_scale = [0.5 if is_xl else 1.0] * len(args.controlnet_type)
    elif len(args.controlnet_type) != len(args.controlnet_scale):
        raise ValueError(
            f"Numbers of controlnet_type {len(args.controlnet_type)} should be equal to number of controlnet_scale {len(args.controlnet_scale)}."
        )

    # Convert controlnet scales to tensor
    controlnet_scale = torch.FloatTensor(args.controlnet_scale)

    if is_xl:
        images = process_controlnet_images_xl(args)
    else:
        images = []
        for i, image in enumerate(args.controlnet_image):
            images.append(process_controlnet_image(args.controlnet_type[i], Image.open(image), args.height, args.width))

    return images, controlnet_scale

