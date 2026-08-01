
def _save_netpbm(im: Image.Image, fp: IO[bytes], filename: str | bytes) -> None:
    # Unused by default.
    # To use, uncomment the register_save call at the end of the file.
    #
    # If you need real GIF compression and/or RGB quantization, you
    # can use the external NETPBM/PBMPLUS utilities.  See comments
    # below for information on how to enable this.
    tempfile = im._dump()

    try:
        with open(filename, "wb") as f:
            if im.mode != "RGB":
                subprocess.check_call(
                    ["ppmtogif", tempfile], stdout=f, stderr=subprocess.DEVNULL
                )
            else:
                # Pipe ppmquant output into ppmtogif
                # "ppmquant 256 %s | ppmtogif > %s" % (tempfile, filename)
                quant_cmd = ["ppmquant", "256", tempfile]
                togif_cmd = ["ppmtogif"]
                quant_proc = subprocess.Popen(
                    quant_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
                )
                togif_proc = subprocess.Popen(
                    togif_cmd,
                    stdin=quant_proc.stdout,
                    stdout=f,
                    stderr=subprocess.DEVNULL,
                )

                # Allow ppmquant to receive SIGPIPE if ppmtogif exits
                assert quant_proc.stdout is not None
                quant_proc.stdout.close()

                retcode = quant_proc.wait()
                if retcode:
                    raise subprocess.CalledProcessError(retcode, quant_cmd)

                retcode = togif_proc.wait()
                if retcode:
                    raise subprocess.CalledProcessError(retcode, togif_cmd)
    finally:
        try:
            os.unlink(tempfile)
        except OSError:
            pass

