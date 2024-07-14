import os
import logging
import json
from safetensors import safe_open
from safetensors.torch import save_file

logger = logging.getLogger(__name__)

def merge_safetensors_files(directory):
    json_file_name = "config.json"
    json_file_path = os.path.join(directory, json_file_name)
    if not os.path.exists(json_file_path):
        return

    # Step 2: Load the JSON file and extract the weight map
    with open(json_file_path, "r") as file:
        data = json.load(file)
        weight_map = data.get("weight_map")
        if weight_map is None:
            raise KeyError("'weight_map' key not found in the JSON file.")

    # Collect all unique safetensors files from weight_map
    files_to_load = set(weight_map.values())
    all_tensors = {}

    # Load tensors from each unique file
    for file_name in files_to_load:
        part_file_path = os.path.join(directory, file_name)
        if not os.path.exists(part_file_path):
            raise FileNotFoundError(f"Part file {file_name} not found.")

        with safe_open(part_file_path, framework="pt", device="cpu") as f:
            for tensor_key in f.keys():
                if tensor_key in weight_map:
                    all_tensors[tensor_key] = f.get_tensor(tensor_key)

    # Step 4: Save all loaded tensors into a single new safetensors file
    output_file_path = os.path.join(directory, "merged_model.safetensors")
    save_file(all_tensors, output_file_path)

    # Step 5: If the file now exists, remove the index and part files
    if os.path.exists(output_file_path):
        os.remove(json_file_path)
        for file_name in files_to_load:
            os.remove(os.path.join(directory, file_name))

    logger.info(f"All tensors have been merged and saved into {output_file_path}")

print("Write path to checkpoint folder:")
sharded_model_path = input()

merge_safetensors_files(sharded_model_path)