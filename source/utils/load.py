import os
import json

def load_config(path="busybox.json"):
    with open(path, "r") as f:
        return json.load(f)