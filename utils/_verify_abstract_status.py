
def _verify_abstract_status(stub: nodes.FuncDef, runtime: Any) -> Iterator[str]:
    stub_abstract = stub.abstract_status == nodes.IS_ABSTRACT
    runtime_abstract = getattr(runtime, "__isabstractmethod__", False)
    # The opposite can exist: some implementations omit `@abstractmethod` decorators
    if runtime_abstract and not stub_abstract:
        item_type = "property" if stub.is_property else "method"
        yield f"is inconsistent, runtime {item_type} is abstract but stub is not"

