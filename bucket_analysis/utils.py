import numpy as np

def normalize(input) -> dict:
    """
    Attributes:
        values (dict): A map of keys to values, where values can be probabilities or integer/float occurences.
    """
    keys = list(input.keys())
    values = list(input.values())

    np_values = np.array(values)
    total = np.sum(np_values)
    if total == 0:
        raise ValueError("The sum of the values must not be zero.")
    np_values = np_values / total
    np_values = [float(v) for v in np_values]
    return {keys[i]: np_values[i] for i in range(len(keys))}