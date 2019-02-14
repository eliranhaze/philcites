import cPickle as cpkl
import os

def save(data, name):
    filename = _format_filename(name)
    cpkl.dump(data, open(filename, 'wb'))

def load(name, default = None):
    filename = _format_filename(name)
    if os.path.exists(filename):
        data = cpkl.load(open(filename, 'rb'))
        return data
    return default

def _format_filename(name):
    return '.%s.pkl' % name
