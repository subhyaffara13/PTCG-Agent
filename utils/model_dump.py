
def model_dump(
    model: pydantic.BaseModel,
    *,
    exclude: IncEx | None = None,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    warnings: bool = True,
    mode: Literal["json", "python"] = "python",
    by_alias: bool | None = None,
) -> dict[str, Any]:
    if (not PYDANTIC_V1) or hasattr(model, "model_dump"):
        kwargs: _ModelDumpKwargs = {}
        if by_alias is not None:
            kwargs["by_alias"] = by_alias
        return model.model_dump(
            mode=mode,
            exclude=exclude,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            # warnings are not supported in Pydantic v1
            warnings=True if PYDANTIC_V1 else warnings,
            **kwargs,
        )
    return cast(
        "dict[str, Any]",
        model.dict(  # pyright: ignore[reportDeprecated, reportUnnecessaryCast]
            exclude=exclude, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, by_alias=bool(by_alias)
        ),
    )

