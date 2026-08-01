
def get_cutlass_operation_serializer() -> CUTLASSOperationSerializer | None:
    if not try_import_cutlass():
        return None
    return CUTLASSOperationSerializer()

