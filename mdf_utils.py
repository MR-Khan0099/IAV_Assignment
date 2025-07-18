import asammdf
import pandas as pd
import numpy as np

def load_mdf_signals(file_path: str, signal_names: list):
    """
    Loads specified signals from an MDF file into a pandas DataFrame.
    Pads shorter arrays with NaN so all columns have the same length.
    """
    try:
        mdf = asammdf.MDF(file_path)
        data = {}
        max_len = 0
        # First, get all signal samples and find the max length
        for signal_name in signal_names:
            if signal_name in mdf.channels_db:
                signal = mdf.get(signal_name)
                samples = signal.samples
                data[signal_name] = samples
                if len(samples) > max_len:
                    max_len = len(samples)
            else:
                print(f"Warning: Signal '{signal_name}' not found in MDF file.")
        # Pad all arrays to max_len
        for key in data:
            if len(data[key]) < max_len:
                data[key] = np.pad(data[key], (0, max_len - len(data[key])), constant_values=np.nan)
        mdf.close()
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error loading MDF file: {e}")
        return None 