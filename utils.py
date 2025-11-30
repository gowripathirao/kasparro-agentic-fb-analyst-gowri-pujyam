import json
import os
import pandas as pd
from datetime import datetime

def load_data(path):
    df = pd.read_csv(path)
    return df

def save_json(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def now_str():
    return datetime.utcnow().isoformat() + 'Z'
