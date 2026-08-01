
def _get_url_from_router(router, purl):
    if purl:
        try:
            return router.process(purl)
        except NoRouteAvailable:
            return

