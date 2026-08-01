
def run_demo(
    sam2_dir: str,
    model_type: str = "sam2_hiera_large",
    engine: str = "torch",
    dtype: torch.dtype = torch.float32,
    image_encoder_onnx_path: str = "",
    image_decoder_onnx_path: str = "",
    image_decoder_multi_onnx_path: str = "",
    use_gpu: bool = True,
    enable_batch: bool = False,
):
    if use_gpu:
        assert torch.cuda.is_available()
        assert "CUDAExecutionProvider" in onnxruntime.get_available_providers()
        provider = "CUDAExecutionProvider"
    else:
        provider = "CPUExecutionProvider"

    device = torch.device("cuda" if use_gpu else "cpu")

    if use_gpu and engine == "torch" and torch.cuda.get_device_properties(0).major >= 8:
        # Turn on tfloat32 for Ampere GPUs.
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True

    np.random.seed(3)
    image = Image.open("truck.jpg")
    image = np.array(image.convert("RGB"))

    predictor = get_predictor(
        sam2_dir,
        device,
        dtype,
        model_type,
        engine,
        image_encoder_onnx_path,
        image_decoder_onnx_path,
        image_decoder_multi_onnx_path,
        provider=provider,
    )

    predictor.set_image(image)
    prefix = f"sam2_demo_{engine}_"

    #  The model returns masks, quality predictions for those masks,
    #     and low resolution mask logits that can be passed to the next iteration of prediction.
    #  With multimask_output=True (the default setting), SAM 2 outputs 3 masks, where
    #     scores gives the model's own estimation of the quality of these masks.
    #  For ambiguous prompts such as a single point, it is recommended to use multimask_output=True
    #     even if only a single mask is desired;
    input_point = np.array([[500, 375]])
    input_label = np.array([1])
    masks, scores, logits = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=True,
    )

    sorted_ind = np.argsort(scores)[::-1]
    masks = masks[sorted_ind]
    scores = scores[sorted_ind]
    logits = logits[sorted_ind]

    image_files = []
    show_masks(
        image,
        masks,
        scores,
        point_coords=input_point,
        input_labels=input_label,
        borders=True,
        output_image_file_prefix=prefix + "multimask",
        image_files=image_files,
    )

    # Multiple points.
    input_point = np.array([[500, 375], [1125, 625]])
    input_label = np.array([1, 1])
    mask_input = logits[np.argmax(scores), :, :]  # Choose the model's best mask
    masks, scores, _ = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        mask_input=mask_input[None, :, :],
        multimask_output=False,
    )
    show_masks(
        image,
        masks,
        scores,
        point_coords=input_point,
        input_labels=input_label,
        output_image_file_prefix=prefix + "multi_points",
        image_files=image_files,
    )

    # Specify a window and a background point.
    input_point = np.array([[500, 375], [1125, 625]])
    input_label = np.array([1, 0])
    mask_input = logits[np.argmax(scores), :, :]  # Choose the model's best mask
    masks, scores, _ = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        mask_input=mask_input[None, :, :],
        multimask_output=False,
    )
    show_masks(
        image,
        masks,
        scores,
        point_coords=input_point,
        input_labels=input_label,
        output_image_file_prefix=prefix + "background_point",
        image_files=image_files,
    )

    # Take a box as input
    input_box = np.array([425, 600, 700, 875])
    masks, scores, _ = predictor.predict(
        point_coords=None,
        point_labels=None,
        box=input_box[None, :],
        multimask_output=False,
    )
    show_masks(
        image,
        masks,
        scores,
        box_coords=input_box,
        output_image_file_prefix=prefix + "box",
        image_files=image_files,
    )

    # Combining points and boxes
    input_box = np.array([425, 600, 700, 875])
    input_point = np.array([[575, 750]])
    input_label = np.array([0])

    masks, scores, logits = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        box=input_box,
        multimask_output=False,
    )
    show_masks(
        image,
        masks,
        scores,
        box_coords=input_box,
        point_coords=input_point,
        input_labels=input_label,
        output_image_file_prefix=prefix + "box_and_point",
        image_files=image_files,
    )

    # TODO: support batched prompt inputs
    if enable_batch:
        input_boxes = np.array(
            [
                [75, 275, 1725, 850],
                [425, 600, 700, 875],
                [1375, 550, 1650, 800],
                [1240, 675, 1400, 750],
            ]
        )
        masks, scores, _ = predictor.predict(
            point_coords=None,
            point_labels=None,
            box=input_boxes,
            multimask_output=False,
        )
        plt.figure(figsize=(10, 10))
        plt.imshow(image)
        for mask in masks:
            show_mask(mask.squeeze(0), plt.gca(), random_color=True)
        for box in input_boxes:
            show_box(box, plt.gca())
        plt.axis("off")
        plt.show()
        plt.savefig(prefix + "batch_prompt.png")
        image_files.append(prefix + "batch_prompt.png")
    return image_files


def run_demo(args):
    """Run Stable Diffusion XL Base + Refiner together (known as ensemble of expert denoisers) to generate an image."""
    controlnet_image, controlnet_scale = process_controlnet_arguments(args)
    prompt, negative_prompt = repeat_prompt(args)
    batch_size = len(prompt)
    base, refiner = load_pipelines(args, batch_size)
    run_pipelines(args, base, refiner, prompt, negative_prompt, controlnet_image, controlnet_scale)
    base.teardown()
    if refiner:
        refiner.teardown()

