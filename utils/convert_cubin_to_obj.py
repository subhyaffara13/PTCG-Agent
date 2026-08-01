
def convert_cubin_to_obj(
    cubin_file: str,
    kernel_name: str,
    ld: str,
    objcopy: str,
) -> str:
    obj_file = cubin_file + ".o"
    # Convert .cubin to .o
    cmd = f"{ld} -r -b binary -z noexecstack -o {obj_file} {cubin_file}"
    subprocess.run(cmd.split(), capture_output=True, text=True, check=True)
    # Rename .data to .rodata
    cmd = f"{objcopy} --rename-section .data=.rodata,alloc,load,readonly,data,contents {obj_file}"
    subprocess.run(cmd.split(), capture_output=True, text=True, check=True)
    # By default objcopy will create *_start, *_size, *_end symbols using the full path
    # Rename to use the unique kernel name
    file_name = re.sub(r"[\W]", "_", cubin_file)
    cmd = (
        objcopy
        + f" --redefine-sym _binary_{file_name}_start=__{kernel_name}_start "
        + f"--redefine-sym _binary_{file_name}_size=__{kernel_name}_size "
        + f"--redefine-sym _binary_{file_name}_end=__{kernel_name}_end "
        + obj_file
    )
    subprocess.run(cmd.split(), capture_output=True, text=True, check=True)
    return obj_file

