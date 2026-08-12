import numpy as np
from scipy.stats import skew, kurtosis


def extract_advanced_features(signal):

    signal = np.array(signal)

    features = {}

    # Basic features
    features["mean"] = np.mean(signal)
    features["std"] = np.std(signal)
    features["min"] = np.min(signal)
    features["max"] = np.max(signal)
    features["range"] = np.max(signal) - np.min(signal)
    features["rms"] = np.sqrt(np.mean(signal**2))

    # Advanced features
    features["energy"] = np.sum(signal**2)

    features["variance"] = np.var(signal)

    features["skewness"] = skew(signal)

    features["kurtosis"] = kurtosis(signal)

    # Signal change features
    diff = np.diff(signal)

    features["mean_change"] = np.mean(np.abs(diff))

    features["max_change"] = np.max(np.abs(diff))

    return features