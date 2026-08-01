
def get_web_endpoint(env: KaggleEnv):
    # In PROD, the `api` subdomain is used which breaks link to detail pages.
    if env == KaggleEnv.PROD:
        return "https://kaggle.com"
    return get_endpoint(env)

