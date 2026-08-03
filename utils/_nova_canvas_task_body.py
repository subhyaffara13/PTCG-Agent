from typing import Any, Dict, Optional

def _nova_canvas_task_body(
    *,
    image_b64: str,
    mask_b64: Optional[str],
    text: str,
    negative_text: Optional[str],
    similarity_strength: Optional[float],
    task_type: Optional[str],
    mask_prompt: Optional[str],
    out_painting_mode: Optional[str],
) -> Dict[str, Any]:
    """Build InvokeModel body task section (without imageGenerationConfig)."""
    if task_type == "BACKGROUND_REMOVAL":
        return {
            "taskType": "BACKGROUND_REMOVAL",
            "backgroundRemovalParams": {"image": image_b64},
        }
    if task_type == "OUTPAINTING":
        if mask_prompt is None and mask_b64 is None:
            raise ValueError(
                "OUTPAINTING requires either a mask image or a mask prompt. "
                "Pass mask=<file> or maskPrompt=<str> in the request."
            )
        out_params: Dict[str, Any] = {
            "image": image_b64,
            "text": text,
        }
        if mask_prompt is not None:
            out_params["maskPrompt"] = mask_prompt
        elif mask_b64 is not None:
            out_params["maskImage"] = mask_b64
        if negative_text is not None:
            out_params["negativeText"] = negative_text
        if out_painting_mode is not None:
            out_params["outPaintingMode"] = out_painting_mode
        return {
            "taskType": "OUTPAINTING",
            "outPaintingParams": out_params,
        }
    # Honour explicit IMAGE_VARIATION even when a mask is present (mask is ignored
    # for this task type; callers use INPAINTING when they want mask semantics).
    if task_type == "IMAGE_VARIATION":
        var_params_explicit: Dict[str, Any] = {
            "images": [image_b64],
            "text": text,
        }
        if negative_text is not None:
            var_params_explicit["negativeText"] = negative_text
        if similarity_strength is not None:
            var_params_explicit["similarityStrength"] = similarity_strength
        return {
            "taskType": "IMAGE_VARIATION",
            "imageVariationParams": var_params_explicit,
        }
    # Explicit taskType must be INPAINTING or omitted from here on; anything else is invalid.
    if task_type is not None and str(task_type).strip() != "":
        if task_type != "INPAINTING":
            raise ValueError(
                f"Unsupported Amazon Nova Canvas taskType: {task_type!r}. "
                "Use BACKGROUND_REMOVAL, OUTPAINTING, IMAGE_VARIATION, INPAINTING, "
                "or omit taskType for automatic routing (mask → INPAINTING, else IMAGE_VARIATION)."
            )
    if mask_b64 is not None or mask_prompt is not None or task_type == "INPAINTING":
        in_params: Dict[str, Any] = {"image": image_b64, "text": text}
        if mask_prompt is not None:
            in_params["maskPrompt"] = mask_prompt
        elif mask_b64 is not None:
            in_params["maskImage"] = mask_b64
        if negative_text is not None:
            in_params["negativeText"] = negative_text
        if "maskPrompt" not in in_params and "maskImage" not in in_params:
            raise ValueError(
                "Amazon Nova Canvas INPAINTING requires either maskPrompt or maskImage "
                "(use OpenAI mask= for maskImage, or pass maskPrompt in optional params). "
                "See https://docs.aws.amazon.com/nova/latest/userguide/image-gen-req-resp-structure.html"
            )
        return {"taskType": "INPAINTING", "inPaintingParams": in_params}
    var_params: Dict[str, Any] = {
        "images": [image_b64],
        "text": text,
    }
    if negative_text is not None:
        var_params["negativeText"] = negative_text
    if similarity_strength is not None:
        var_params["similarityStrength"] = similarity_strength
    return {
        "taskType": "IMAGE_VARIATION",
        "imageVariationParams": var_params,
    }

