
def compiler_wrapper(request):
    class CompilerWrapper(unix.Compiler):
        def rpath_foo(self):
            return self.runtime_library_dir_option('/foo')

    request.instance.cc = CompilerWrapper()

