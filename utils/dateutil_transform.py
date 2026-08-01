
def dateutil_transform() -> nodes.Module:
    return AstroidBuilder(AstroidManager()).string_build(
        textwrap.dedent(
            """
    import datetime
    def parse(timestr, parserinfo=None, **kwargs):
        return datetime.datetime()
    """
        )
    )

