
def _azure_image_url_helper(content: ChatCompletionImageObject):
    if isinstance(content["image_url"], str):
        content["image_url"] = {"url": content["image_url"]}
    return

