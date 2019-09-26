import pickle
import os
import sys

# Wrappers for loading/saving pickle files
def load_pickle_file(filepath):
    if(os.path.isfile(filepath)):
        with open(filepath, "rb") as p:
            hs = pickle.load(p)
        return hs
    return None

def save_pickle_file(data, filename):
    with open(filename, "wb") as p:
        pickle.dump(data, p, protocol=pickle.HIGHEST_PROTOCOL)
