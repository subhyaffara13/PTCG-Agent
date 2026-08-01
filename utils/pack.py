
def pack(o, stream, **kwargs):
    """
    Pack object `o` and write it to `stream`

    See :class:`Packer` for options.
    """
    packer = Packer(**kwargs)
    stream.write(packer.pack(o))


def pack(fmt: bytes | str, /, *v: Any) -> bytes:
    return struct.pack(fmt, *v)


def pack(directory: str, dest_dir: str, build_number: str | None) -> None:
    """Repack a previously unpacked wheel directory into a new wheel file.

    The .dist-info/WHEEL file must contain one or more tags so that the target
    wheel file name can be determined.

    :param directory: The unpacked wheel directory
    :param dest_dir: Destination directory (defaults to the current directory)
    """
    # Find the .dist-info directory
    dist_info_dirs = [
        fn
        for fn in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, fn)) and DIST_INFO_RE.match(fn)
    ]
    if len(dist_info_dirs) > 1:
        raise WheelError(f"Multiple .dist-info directories found in {directory}")
    elif not dist_info_dirs:
        raise WheelError(f"No .dist-info directories found in {directory}")

    # Determine the target wheel filename
    dist_info_dir = dist_info_dirs[0]
    name_version = DIST_INFO_RE.match(dist_info_dir).group("namever")

    # Read the tags and the existing build number from .dist-info/WHEEL
    wheel_file_path = os.path.join(directory, dist_info_dir, "WHEEL")
    with open(wheel_file_path, "rb") as f:
        info = BytesParser(policy=email.policy.compat32).parse(f)
        tags: list[str] = info.get_all("Tag", [])
        existing_build_number = info.get("Build")

        if not tags:
            raise WheelError(
                f"No tags present in {dist_info_dir}/WHEEL; cannot determine target "
                f"wheel filename"
            )

    # Set the wheel file name and add/replace/remove the Build tag in .dist-info/WHEEL
    build_number = build_number if build_number is not None else existing_build_number
    if build_number is not None:
        del info["Build"]
        if build_number:
            info["Build"] = build_number
            name_version += "-" + build_number

        if build_number != existing_build_number:
            with open(wheel_file_path, "wb") as f:
                BytesGenerator(f, maxheaderlen=0).flatten(info)

    # Reassemble the tags for the wheel file
    tagline = compute_tagline(tags)

    # Repack the wheel
    wheel_path = os.path.join(dest_dir, f"{name_version}-{tagline}.whl")
    with WheelFile(wheel_path, "w") as wf:
        print(f"Repacking wheel as {wheel_path}...", end="", flush=True)
        wf.write_files(directory)

    print("OK")


def pack(o, stream, **kwargs):
    """
    Pack object `o` and write it to `stream`

    See :class:`Packer` for options.
    """
    packer = Packer(**kwargs)
    stream.write(packer.pack(o))


def pack(*xs, dtype):
  return pack_dtype_p.bind(*xs, dtype=dtype)


def pack(
    a: jax.Array,
    b: jax.Array,
    /,
    *,
    format: PackFormat,
    preferred_element_type: jax.typing.DTypeLike | None = None,
) -> jax.Array:
  """Packs two arrays according to the given format.

  .. warning:: This API is temporary and will be removed once the SparseCore
               compiler is able to do packing/unpacking automatically.

  Args:
    a: The first array to pack.
    b: The second array to pack.
    format: The packing format to use.
    preferred_element_type: Optional. The preferred element type of the packed
      array. If specified, must have half the bitwidth of the input array types.

  Returns:
    The packed array.
  """
  if preferred_element_type is not None:
    preferred_element_type = jnp.dtype(preferred_element_type)
  return pack_p.bind(
      a, b, format=format, preferred_element_type=preferred_element_type
  )


def pack(
    msg: Message,
    type_url_prefix: Optional[str] = 'type.googleapis.com/',
    deterministic: Optional[bool] = None,
) -> Any:
  any_msg = Any()
  any_msg.Pack(
      msg=msg, type_url_prefix=type_url_prefix, deterministic=deterministic
  )
  return any_msg


def pack(fmt, obj):
    formatstring, names, fixes = getformat(fmt, keep_pad_byte=True)
    elements = []
    if not isinstance(obj, dict):
        obj = obj.__dict__
    for name in names.keys():
        value = obj[name]
        if name in fixes:
            # fixed point conversion
            value = fl2fi(value, fixes[name])
        elif isinstance(value, str):
            value = tobytes(value)
        elements.append(value)
        # Check it fits
        try:
            struct.pack(names[name], value)
        except Exception as e:
            raise ValueError(
                "Value %s does not fit in format %s for %s" % (value, names[name], name)
            ) from e
    data = struct.pack(*(formatstring,) + tuple(elements))
    return data


def pack(
    fn: Callable[..., Any],
    in_variable_filters: Sequence[CollectionFilter],
    out_variable_filters: Sequence[CollectionFilter],
    rng_filters: Sequence[PRNGSequenceFilter],
    name=None,
    enable_kwargs=False,
) -> Callable[..., Any]:
  """Pack variables and rngs for functional transformations.

  The pack function is the building block for all other lifted transformations.

  Args:
    fn: The function to pack. `fn` has the signature
      `(scope_fn, repack_fn, variable_groups, rng_groups, *args) ->
      (output, packed_variables)`.
    in_variable_filters: Input variable filters.
    out_variable_filters: Output variable filters.
    rng_filters: RNG filters.
    name: The name of the packed scope.
    enable_kwargs: Whether to enable kwargs or not.
  Returns:
    A callable which expects a scope as the first argument.
  """

  @functools.wraps(fn)
  def wrapper(scope_tree: Scope, *args, **kwargs):
    if not enable_kwargs and kwargs:
      msg = 'kwargs are not supported in {}, so "{}" is(are) ignored'
      warnings.warn(msg.format(name, ', '.join(kwargs.keys())), RuntimeWarning)
    (
        scope_fn,
        repack_fn,
        variable_groups_xs_t,
        rng_groups_xs_t,
        publish_results_fn,
    ) = _partial_pack(scope_tree, in_variable_filters, out_variable_filters, rng_filters, name)
    if enable_kwargs:
      y, out_variable_groups_xs_t = fn(
          scope_fn,
          repack_fn,
          variable_groups_xs_t,
          rng_groups_xs_t,
          *args,
          **kwargs,
      )
    else:
      y, out_variable_groups_xs_t = fn(
          scope_fn, repack_fn, variable_groups_xs_t, rng_groups_xs_t, *args
      )
    publish_results_fn(out_variable_groups_xs_t)
    return y

  return wrapper

