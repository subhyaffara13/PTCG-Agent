from typing import Any

def make_ktc_generator(
    template: KernelTemplate | ExternKernelChoice,
    cs: Generator[KernelTemplateParams, None, None],
    extra_kwargs: dict[str, Any],
    overrides: dict[str, Any],
    layout: Layout,
    inputs: KernelInputs,
) -> Generator[KernelTemplateChoice, None, None]:
    """
    Create a generator of KernelTemplateChoice objects for a given template.

    Args:
        template: The template object (KernelTemplate or ExternKernelChoice)
        cs: Generator of KernelTemplateParams from template heuristic
        overrides: Override kwargs for the template
        layout: Layout value for the template
        inputs: KernelInputs for the op

    Yields:
        KernelTemplateChoice objects
    """
    for params in cs:
        # Apply overrides to params
        base_kwargs = params.to_kwargs()
        final_kwargs = {**base_kwargs, **overrides}
        final_params = DictKernelTemplateParams(final_kwargs)
        yield KernelTemplateChoice(
            template=template,
            params=final_params,
            extra_kwargs=extra_kwargs,
            layout=layout,
            inputs=inputs,
        )

