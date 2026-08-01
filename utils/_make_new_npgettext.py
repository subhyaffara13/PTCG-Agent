
def _make_new_npgettext(
    func: t.Callable[[str, str, str, int], str],
) -> t.Callable[..., str]:
    @pass_context
    def npgettext(
        __context: Context,
        __string_ctx: str,
        __singular: str,
        __plural: str,
        __num: int,
        **variables: t.Any,
    ) -> str:
        variables.setdefault("context", __string_ctx)
        variables.setdefault("num", __num)
        rv = __context.call(func, __string_ctx, __singular, __plural, __num)

        if __context.eval_ctx.autoescape:
            rv = Markup(rv)

        # Always treat as a format string, see gettext comment above.
        return rv % variables  # type: ignore

    return npgettext

