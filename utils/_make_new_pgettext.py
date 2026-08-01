
def _make_new_pgettext(func: t.Callable[[str, str], str]) -> t.Callable[..., str]:
    @pass_context
    def pgettext(
        __context: Context, __string_ctx: str, __string: str, **variables: t.Any
    ) -> str:
        variables.setdefault("context", __string_ctx)
        rv = __context.call(func, __string_ctx, __string)

        if __context.eval_ctx.autoescape:
            rv = Markup(rv)

        # Always treat as a format string, see gettext comment above.
        return rv % variables  # type: ignore

    return pgettext

