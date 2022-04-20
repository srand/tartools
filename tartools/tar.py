from contextlib import contextmanager
import pathlib
import tarfile

from tartools import utils
from tartools.tree import Inode, Tree, WhiteoutInode


class TarTree(Tree):
    def __init__(self, path, mode):
        self._path = path
        self._tarfile = tarfile.open(path, mode)

    def __iter__(self):
        for tarinfo in self._tarfile.getmembers():
            name = utils.from_whiteout_path(tarinfo.name)
            if name != tarinfo.name:
                yield WhiteoutInode(self._path, name)
            else:
                yield TarInode(tarinfo)

    def __getitem__(self, path):
        name = utils.from_whiteout_path(path)
        if name != path:
            return WhiteoutInode(self._path, name)
        else:
            tarinfo = self._tarfile.getmember(path)
            return TarInode(tarinfo)

    def _as_tarinfo(self, inode):
        ti = tarfile.TarInfo(inode.path)
        ti.uid = inode.uid
        ti.gid = inode.gid
        ti.linkname = inode.linkpath
        ti.mode = inode.mode
        ti.mtime = inode.mtime
        ti.size = inode.size
        if inode.is_symlink():
            ti.type = tarfile.SYMTYPE
        elif inode.is_dir():
            ti.type = tarfile.DIRTYPE
        else:
            ti.type = tarfile.REGTYPE
        return ti

    def add(self, inode, fileobj=None):
        tarinode = self._as_tarinfo(inode)
        self._tarfile.addfile(tarinode, fileobj)

    def add_whiteout(self, inode):
        tarinode = self._as_tarinfo(inode)
        tarinode.name = utils.whiteout_path(inode.path)
        self._tarfile.addfile(tarinode)

    @contextmanager
    def read(self, inode):
        fileobj = None
        try:
            fileobj = self._tarfile.extractfile(inode.path)
            yield fileobj
        finally:
            if fileobj is not None:
                fileobj.close()

    def close(self):
        self._tarfile.close()


class TarInode(Inode):
    def __init__(self, tarinfo):
        self._tarinfo = tarinfo
        self._size = None

    def is_dir(self):
        return self._tarinfo.isdir()

    def is_file(self):
        return self._tarinfo.isfile()

    def is_symlink(self):
        return self._tarinfo.issym()

    def is_parent_of(self, path):
        return pathlib.Path(path).is_relative_to(self._tarinfo.name)

    @property
    def gid(self):
        return self._tarinfo.gid

    @property
    def linkpath(self):
        return self._tarinfo.linkname

    @property
    def mode(self):
        return self._tarinfo.mode

    @property
    def mtime(self):
        return self._tarinfo.mtime

    @property
    def path(self):
        return self._tarinfo.name

    @property
    def size(self):
        return self._size or self._tarinfo.size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def uid(self):
        return self._tarinfo.uid
