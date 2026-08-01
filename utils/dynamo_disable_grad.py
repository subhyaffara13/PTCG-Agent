
def dynamo_disable_grad(tx: "InstructionTranslator") -> typing.Iterator[None]:
    from . import GradModeVariable

    gmv = GradModeVariable.create(tx, False)
    try:
        gmv.enter(tx)
        yield
    finally:
        gmv.exit(tx)

