
def _gemini_vision_convert_messages(messages: list):
    """
    Converts given messages for GPT-4 Vision to Gemini format.

    Args:
        messages (list): The messages to convert. Each message can be a dictionary with a "content" key. The content can be a string or a list of elements. If it is a string, it will be concatenated to the prompt. If it is a list, each element will be processed based on its type:
            - If the element is a dictionary with a "type" key equal to "text", its "text" value will be concatenated to the prompt.
            - If the element is a dictionary with a "type" key equal to "image_url", its "image_url" value will be added to the list of images.

    Returns:
        tuple: A tuple containing the prompt (a string) and the processed images (a list of objects representing the images).
    """

    try:
        # given messages for gpt-4 vision, convert them for gemini
        # https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/getting-started/intro_gemini_python.ipynb
        prompt = ""
        images = []
        for message in messages:
            if isinstance(message["content"], str):
                prompt += message["content"]
            elif isinstance(message["content"], list):
                # see https://docs.litellm.ai/docs/providers/openai#openai-vision-models
                for element in message["content"]:
                    if isinstance(element, dict):
                        if element["type"] == "text":
                            prompt += element["text"]
                        elif element["type"] == "image_url":
                            image_url = element["image_url"]["url"]
                            images.append(image_url)
        # processing images passed to gemini
        processed_images = []
        for img in images:
            if "https:/" in img:
                # Case 1: Image from URL
                image = _load_image_from_url(img)
                processed_images.append(image)

            else:
                try:
                    from PIL import Image
                except Exception:
                    raise Exception(
                        "gemini image conversion failed please run `pip install Pillow`"
                    )

                if "base64" in img:
                    # Case 2: Base64 image data
                    import base64
                    import io

                    # Extract the base64 image data
                    base64_data = img.split("base64,")[1]

                    # Decode the base64 image data
                    image_data = base64.b64decode(base64_data)

                    # Load the image from the decoded data
                    image = Image.open(io.BytesIO(image_data))
                else:
                    # Case 3: Image filepath (e.g. temp.jpeg) given
                    image = Image.open(img)
                processed_images.append(image)
        content = [prompt] + processed_images
        return content
    except Exception as e:
        raise e

