
def _mesh_get_process_group_fake(mesh, dim):
    from torch._library.fake_class_registry import maybe_unwrap_fake_script_object

    real_mesh = maybe_unwrap_fake_script_object(mesh)
    return real_mesh.get_group(dim)

