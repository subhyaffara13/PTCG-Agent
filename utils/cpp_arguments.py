
def cpp_arguments(f: NativeFunction) -> Sequence[Binding]:
    sigs = CppSignatureGroup.from_native_function(f, method=False)
    if sigs.symint_signature is not None:
        return sigs.symint_signature.arguments()
    else:
        return sigs.signature.arguments()

