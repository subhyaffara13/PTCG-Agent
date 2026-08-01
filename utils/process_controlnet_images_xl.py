
def process_controlnet_images_xl(args) -> list[Image.Image]:
    """
    Process control image for SDXL control net.
    """
    assert len(args.controlnet_image) == 1
    image = Image.open(args.controlnet_image[0]).convert("RGB")

    controlnet_images = []
    if args.controlnet_type[0] == "canny":
        controlnet_images.append(get_canny_image(image))
    elif args.controlnet_type[0] == "depth":
        controlnet_images.append(get_depth_image(image))
    else:
        raise ValueError(f"This controlnet type is not supported for SDXL or Turbo: {args.controlnet_type}.")

    return controlnet_images

