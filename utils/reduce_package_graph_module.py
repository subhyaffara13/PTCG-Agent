from typing import Any

def reduce_package_graph_module(
    importer: PackageImporter, body: dict[Any, Any], generated_module_name: str
) -> torch.nn.Module:
    forward = importer.import_module(generated_module_name).forward
    return _deserialize_graph_module(forward, body)

