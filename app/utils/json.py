# app/utils/json.py
import numpy as np

def make_json_safe(data):
    """Convert numpy types (ndarray, float32, int64, etc.) into JSON-safe types."""
    if isinstance(data, np.ndarray):
        return data.tolist()
    if isinstance(data, (np.float32, np.float64)):
        return float(data)
    if isinstance(data, (np.int32, np.int64)):
        return int(data)
    if isinstance(data, list):
        return [make_json_safe(x) for x in data]
    if isinstance(data, dict):
        return {k: make_json_safe(v) for k, v in data.items()}
    return data
