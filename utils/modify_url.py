
def modify_url(original_url, new_path):
    url = httpx.URL(original_url)
    modified_url = url.copy_with(path=new_path)
    return str(modified_url)

