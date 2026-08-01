
def _build_output_specs(
    mesh: DeviceMesh,
    per_mesh_dim_placements: list[tuple[Placement | None, ...]],
    num_outputs: int,
    output_metas: tuple[TensorMeta | None, ...],
) -> DTensorSpec | tuple[DTensorSpec | None, ...]:
    """Build output spec(s) by transposing per-mesh-dim placements to per-output.

    per_mesh_dim_placements is indexed [mesh_dim][output_idx]. output_metas must
    have exactly num_outputs elements. Outputs where output_metas[i] is None
    (masked-off outputs) produce None specs.
    """
    if num_outputs <= 0:
        raise AssertionError(f"Expected num_outputs > 0, got {num_outputs}")
    if len(output_metas) != num_outputs:
        raise AssertionError(
            f"Expected {num_outputs} output_metas, got {len(output_metas)}"
        )

    def _spec_for_output(out_idx: int) -> DTensorSpec | None:
        if output_metas[out_idx] is None:
            return None
        placements = tuple(
            cast(Placement, out[out_idx]) for out in per_mesh_dim_placements
        )
        return DTensorSpec(mesh, placements, tensor_meta=output_metas[out_idx])

    if num_outputs > 1:
        return tuple(_spec_for_output(i) for i in range(num_outputs))
    else:
        spec = _spec_for_output(0)
        if spec is None:
            raise AssertionError("Single-output op cannot have None output meta")
        return spec

