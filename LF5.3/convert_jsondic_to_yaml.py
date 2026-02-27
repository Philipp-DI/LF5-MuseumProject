import json as js
import yaml

with open("museum/sample_entry.json", "r") as json_file:
    data = js.load(json_file)
with open("museum/converted_from_json.yaml", "w") as yaml_file:
    yaml.dump(data, yaml_file)