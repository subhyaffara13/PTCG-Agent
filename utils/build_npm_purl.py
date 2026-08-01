
def build_npm_purl(uri):
    # npm URLs are difficult to disambiguate with regex
    if "/package/" in uri:
        return build_npm_web_purl(uri)
    elif "/-/" in uri:
        return build_npm_download_purl(uri)
    else:
        return build_npm_api_purl(uri)

