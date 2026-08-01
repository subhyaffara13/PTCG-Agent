
def brainless_manager():
    m = manager.AstroidManager()
    # avoid caching into the AstroidManager borg since we get problems
    # with other tests :
    m.__dict__ = {}
    m._failed_import_hooks = []
    m.astroid_cache = {}
    m._mod_file_cache = {}
    m._transform = transforms.TransformVisitor()
    m.extension_package_whitelist = set()
    m.module_denylist = set()
    return m

