from contextlib import contextmanager
import os
import shutil
import stat

from tartools.tree import Tree, Inode


class DirectoryInode(Inode):
    def __init__(self, path, name):
        self._path = name
        self._fullpath = os.path.join(path, name)
        self._stat = os.lstat(self._fullpath)
        self._size = None

    def is_dir(self):
        return stat.S_ISDIR(self._stat.st_mode)

    def is_file(self):
        return stat.S_ISREG(self._stat.st_mode)

    def is_symlink(self):
        return stat.S_ISLNK(self._stat.st_mode)

    @property
    def mode(self):
        return self._stat.st_mode

    @property
    def path(self):
        return self._path

    @property
    def size(self):
        return self._size or self._stat.st_size

    @size.setter
    def size(self, value):
        self._size = value


class DirectoryTree(Tree):
    def __init__(self, path, writable=False):
        self._path = path
        if writable:
            try:
                shutil.rmtree(self._path)
            except FileNotFoundError:
                pass
            os.makedirs(self._path)

    def __iter__(self):
        for root, dirs, files in os.walk(self._path):
            relroot = os.path.relpath(root, self._path)
            if relroot == ".":
                relroot = ""
            for dir in dirs:
                yield DirectoryInode(self._path, os.path.join(relroot, dir))
            for file in files:
                yield DirectoryInode(self._path, os.path.join(relroot, file))

    def __getitem__(self, path):
        try:
            return DirectoryInode(self._path, path)
        except FileNotFoundError:
            raise KeyError(path)

    def add(self, inode, fileobj=None):
        fullpath = os.path.join(self._path, inode.path)
        if inode.is_dir():
            os.mkdir(fullpath, inode.mode)
        elif inode.is_symlink():
            os.symlink(inode.linkpath, fullpath)
            os.chmod(fullpath, inode.mode)
        else:
            with open(fullpath, "wb", inode.mode) as destobj:
                if fileobj:
                    shutil.copyfileobj(fileobj, destobj)

    @contextmanager
    def read(self, inode):
        with open(os.path.join(self._path, inode.path), "rb") as fileobj:
            yield fileobj

    def close(self):
        pass
