
def _set_image_outputs(span: "Span", response_obj, image_attrs, span_attrs):
    images = response_obj.get("data", [])
    for i, image in enumerate(images):
        img_url = image.get("url")
        if img_url is None and image.get("b64_json"):
            img_url = f"data:image/png;base64,{image.get('b64_json')}"

        if not img_url:
            continue

        if i == 0:
            safe_set_attribute(span, span_attrs.OUTPUT_VALUE, img_url)

        safe_set_attribute(span, f"{image_attrs.IMAGE_URL}.{i}", img_url)

