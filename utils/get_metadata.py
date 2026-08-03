import os
import sys
from typing import Any

def get_metadata(args, is_xl: bool = False) -> dict[str, Any]:
    metadata = {
        "command": " ".join(['"' + x + '"' if " " in x else x for x in sys.argv]),
        "args.prompt": args.prompt,
        "args.negative_prompt": args.negative_prompt,
        "args.batch_size": args.batch_size,
        "height": args.height,
        "width": args.width,
        "cuda_graph": not args.disable_cuda_graph,
        "vae_slicing": args.enable_vae_slicing,
        "engine": args.engine,
    }

    if args.lora_weights:
        metadata["lora_weights"] = args.lora_weights
        metadata["lora_scale"] = args.lora_scale

    if args.controlnet_type:
        metadata["controlnet_type"] = args.controlnet_type
        metadata["controlnet_scale"] = args.controlnet_scale

    if is_xl and args.enable_refiner:
        metadata["base.scheduler"] = args.scheduler
        metadata["base.denoising_steps"] = args.denoising_steps
        metadata["base.guidance"] = args.guidance
        metadata["refiner.strength"] = args.strength
        metadata["refiner.scheduler"] = args.refiner_scheduler
        metadata["refiner.denoising_steps"] = args.refiner_denoising_steps
        metadata["refiner.guidance"] = args.refiner_guidance
    else:
        metadata["scheduler"] = args.scheduler
        metadata["denoising_steps"] = args.denoising_steps
        metadata["guidance"] = args.guidance

    # Version of installed python packages
    packages = ""
    for name in [
        "onnxruntime-gpu",
        "torch",
        "tensorrt",
        "transformers",
        "diffusers",
        "onnx",
        "onnx-graphsurgeon",
        "polygraphy",
        "controlnet_aux",
    ]:
        try:
            packages += (" " if packages else "") + f"{name}=={version(name)}"
        except PackageNotFoundError:
            continue
    metadata["packages"] = packages
    metadata["device"] = torch.cuda.get_device_name()
    metadata["torch.version.cuda"] = torch.version.cuda

    return metadata


def get_metadata(key):
  import requests  # pyrefly: ignore[missing-source-for-stubs]
  import time
  # Based on https://github.com/tensorflow/tensorflow/pull/40317
  gce_metadata_endpoint = 'http://' + os.environ.get(
      'GCE_METADATA_IP', 'metadata.google.internal')

  retry_count = 0
  retrySeconds = 0.500
  api_resp = None

  while retry_count < 6:
    api_resp = requests.get(
        f'{gce_metadata_endpoint}/computeMetadata/v1/instance/attributes/{key}',
        headers={'Metadata-Flavor': 'Google'}, timeout=60)
    if api_resp.status_code == 200:
      break
    retry_count += 1
    time.sleep(retrySeconds)

  if api_resp is None:
    raise RuntimeError(f"Getting metadata['{key}'] failed for 6 tries")
  return api_resp.text, api_resp.status_code

