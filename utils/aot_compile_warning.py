
def aot_compile_warning():

    log.warning("+============================+")
    log.warning("|     !!!   WARNING   !!!    |")
    log.warning("+============================+")
    log.warning(
        "torch._export.aot_compile()/torch._export.aot_load() is being deprecated, please switch to "
        "directly calling torch._inductor.aoti_compile_and_package(torch.export.export())/"
        "torch._inductor.aoti_load_package() instead.")

