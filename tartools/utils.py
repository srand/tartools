import os


def pathiter(path, skip=0):
    genpath = ""
    for component in path.split(os.sep)[:-skip]:
        genpath = os.path.join(genpath, component)
        yield genpath


def whiteout_path(path):
    dirname, name = os.path.split(path)
    return os.path.join(dirname, ".wh." + name)


def from_whiteout_path(path):
    dirname, name = os.path.split(path)
    return os.path.join(dirname, name[4:] if name.startswith(".wh.") else name)


def is_whiteout_path(path):
    dirname, name = os.path.split(path)
    return name.startswith(".wh.")
