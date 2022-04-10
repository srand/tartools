import hashlib
import os


class Tree(object):
    def __iter__(self):
        raise NotImplementedError()

    def __getitem__(self, path):
        raise NotImplementedError()

    def checksum(self, item, hashfn=hashlib.sha1):
        with self.read(item) as fileobj:
            h = hashfn()
            for data in iter(lambda: fileobj.read(0x10000), b''):
                h.update(data)
            return h.hexdigest()

    def add(self, item, fileobj=None):
        raise NotImplementedError()

    def add_whiteout(self, item):
        self.add(WhiteoutInode(item))

    def read(self, item):
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
    def __init__(self, item):
        dirname, name = os.path.split(item.path)
        self._path = os.path.join(dirname, ".wh." + name)

    def is_dir(self):
        return False

    def is_file(self):
        return True

    def is_symlink(self):
        return False

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
