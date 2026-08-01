
def _patch_for_embedding(patchlist):
    if sys.platform == 'win32':
        # we must not remove the manifest when building for embedding!
        # FUTURE: this module was removed in setuptools 74; this is likely dead code and should be removed,
        #  since the toolchain it supports (VS2005-2008) is also long dead.
        from cffi._shimmed_dist_utils import MSVCCompiler
        if MSVCCompiler is not None:
            _patch_meth(patchlist, MSVCCompiler, '_remove_visual_c_ref',
                        lambda self, manifest_file: manifest_file)

    if sys.platform == 'darwin':
        # we must not make a '-bundle', but a '-dynamiclib' instead
        from cffi._shimmed_dist_utils import CCompiler
        def my_link_shared_object(self, *args, **kwds):
            if '-bundle' in self.linker_so:
                self.linker_so = list(self.linker_so)
                i = self.linker_so.index('-bundle')
                self.linker_so[i] = '-dynamiclib'
            return old_link_shared_object(self, *args, **kwds)
        old_link_shared_object = _patch_meth(patchlist, CCompiler,
                                             'link_shared_object',
                                             my_link_shared_object)

