
def _cpp_signature(f: NativeFunction, *, method: bool = False) -> CppSignature:
    return CppSignatureGroup.from_native_function(f, method=method).signature

