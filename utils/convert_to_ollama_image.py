
def convert_to_ollama_image(openai_image_url: str):
    try:
        if openai_image_url.startswith("http"):
            openai_image_url = convert_url_to_base64(url=openai_image_url)

        if openai_image_url.startswith("data:image/"):
            # Extract the base64 image data
            base64_data = openai_image_url.split("data:image/")[1].split(";base64,")[1]
        else:
            base64_data = openai_image_url

        return base64_data
    except Exception as e:
        if "Error: Unable to fetch image from URL" in str(e):
            raise e
        raise Exception(
            """Image url not in expected format. Example Expected input - "image_url": "data:image/jpeg;base64,{base64_image}". """
        )

