
def dynamo_enable_grad(
    tx: "InstructionTranslator", enable: bool = True
) -> Generator[None, None, None]:
    from . import GradModeVariable

    org_value = torch.is_grad_enabled()
    try:
        GradModeVariable.create(tx, enable, initialized=True)
        yield
    finally:
        GradModeVariable.create(tx, org_value, initialized=True)

