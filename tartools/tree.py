import hashlib
import os
import pathlib

from tartools import utils


class Tree(object):
    def __iter__(self):
        raise NotImplementedError()

    def __getitem__(self, path):
        raise NotImplementedError()

    def checksum(self, inode, hashfn=hashlib.sha1):
        with self.read(inode) as fileobj:
            h = hashfn()
            for data in iter(lambda: fileobj.read(0x10000), b''):
                h.update(data)
            return h.hexdigest()

    def add(self, inode, fileobj=None):
        raise NotImplementedError()

    def add_whiteout(self, inode):
        raise NotImplementedError()

    def read(self, inode):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()


class Inode(object):
    def is_dir(self):
        raise NotImplementedError()

    def is_file(self):
        raise NotImplementedError()

    def is_symlink(self):
        raise NotImplementedError()

    def is_whiteout(self):
        return utils.is_whiteout_path(self.path)

    def is_parent_of(self, path):
        return pathlib.Path(path).is_relative_to(self._path)

    @property
    def mode(self):
        raise NotImplementedError()

    @property
    def path(self):
        raise NotImplementedError()

    @property
    def size(self):
        raise NotImplementedError()

    @size.setter
    def size(self, value):
        raise NotImplementedError()

    @property
    def type(self):
        raise NotImplementedError()


class WhiteoutInode(object):
    def __init__(self, path, name):
        self._path = name
        self._fullpath = os.path.join(path, name)

    def is_dir(self):
        return False

    def is_file(self):
        return False

    def is_symlink(self):
        return False

    def is_whiteout(self):
        return True

    def is_parent_of(self, path):
        return pathlib.Path(path).is_relative_to(self._path)

    @property
    def gid(self):
        return 0

    @property
    def linkpath(self):
        return ""

    @property
    def mode(self):
        return 0

    @property
    def mtime(self):
        return 0

    @property
    def path(self):
        return self._path

    @property
    def size(self):
        return 0

    @property
    def uid(self):
        return 0
