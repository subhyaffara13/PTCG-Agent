
def unpackage_script_module(
    importer: PackageImporter, script_module_id: str
) -> torch.nn.Module:
    """
    Call by ``torch.package.PackageImporter``'s Pickler's ``persistent_load`` function.

    Performs work of loading and returning a ScriptModule from a ``torch.package`` archive.
    """
    if not isinstance(importer.zip_reader, torch._C.PyTorchFileReader):
        raise RuntimeError(
            "Loading ScriptObjects from a PackageImporter created from a "
            "directory is not supported. Use a package archive file instead."
        )
    cu = torch._C.CompilationUnit()
    cpp_module = torch._C._import_ir_module_from_package(
        cu,
        importer.zip_reader,
        importer.storage_context,
        validate_map_location(importer.last_map_location),
        script_module_id,
    )
    return wrap_cpp_module(cpp_module)

