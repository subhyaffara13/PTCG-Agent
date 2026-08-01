
def save_user_site_setting():
    saved = site.ENABLE_USER_SITE
    try:
        yield saved
    finally:
        site.ENABLE_USER_SITE = saved

