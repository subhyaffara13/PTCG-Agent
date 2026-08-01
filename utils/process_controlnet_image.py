
def process_controlnet_image(controlnet_type: str, image: Image.Image, height, width):
    """
    Process control images of control net v1.1 for Stable Diffusion 1.5.
    """
    control_image = None
    shape = (height, width)
    image = image.convert("RGB")
    if controlnet_type == "canny":
        canny_image = controlnet_aux.CannyDetector()(image)
        control_image = canny_image.resize(shape)
    elif controlnet_type == "normalbae":
        normal_image = controlnet_aux.NormalBaeDetector.from_pretrained("lllyasviel/Annotators")(image)
        control_image = normal_image.resize(shape)
    elif controlnet_type == "depth":
        depth_image = controlnet_aux.LeresDetector.from_pretrained("lllyasviel/Annotators")(image)
        control_image = depth_image.resize(shape)
    elif controlnet_type == "mlsd":
        mlsd_image = controlnet_aux.MLSDdetector.from_pretrained("lllyasviel/Annotators")(image)
        control_image = mlsd_image.resize(shape)
    elif controlnet_type == "openpose":
        openpose_image = controlnet_aux.OpenposeDetector.from_pretrained("lllyasviel/Annotators")(image)
        control_image = openpose_image.resize(shape)
    elif controlnet_type == "scribble":
        scribble_image = controlnet_aux.HEDdetector.from_pretrained("lllyasviel/Annotators")(image, scribble=True)
        control_image = scribble_image.resize(shape)
    elif controlnet_type == "seg":
        seg_image = controlnet_aux.SamDetector.from_pretrained("ybelkada/segment-anything", subfolder="checkpoints")(
            image
        )
        control_image = seg_image.resize(shape)
    else:
        raise ValueError(f"There is no demo image of this controlnet_type: {controlnet_type}")
    return control_image

