from typing import List

def extract_images_from_message(message: AllMessageValues) -> List[str]:
    """
    Extract images from a message.

    For data URLs (e.g., "data:image/png;base64,iVBOR..."), only the base64
    data portion is extracted. This is required for providers like Ollama
    that expect pure base64 data rather than full data URLs.
    """
    images = []
    message_content = message.get("content")
    if isinstance(message_content, list):
        for m in message_content:
            image_url = m.get("image_url")
            if image_url:
                if isinstance(image_url, str):
                    images.append(_extract_base64_data(image_url))
                elif isinstance(image_url, dict) and "url" in image_url:
                    images.append(_extract_base64_data(image_url["url"]))
    return images

