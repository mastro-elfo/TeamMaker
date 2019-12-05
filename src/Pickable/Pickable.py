import pickle

def dump(data, file_name, protocol = pickle.DEFAULT_PROTOCOL):
    """Save `data` to file."""
    with open(file_name, "wb") as fp:
        pickle.dump(data, fp, protocol)

def load(file_name):
    """Load data from file."""
    with open(file_name, 'rb') as fp:
        obj = pickle.load(fp)
    return obj

class Pickable(object):
    def dump(self, file_name, protocol = pickle.DEFAULT_PROTOCOL):
        """Save Pickable object to a file."""
        dump(self, file_name, protocol)

    @staticmethod
    def load(file_name):
        """Return a Pickable object loaded from a file."""
        return load(file_name)
