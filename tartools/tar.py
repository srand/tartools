from contextlib import contextmanager
import tarfile

from tartools.tree import Inode, Tree


class TarTree(Tree):
    def __init__(self, path, mode):
        self._path = path
        self._tarfile = tarfile.open(path, mode)

    def __iter__(self):
        for tarinfo in self._tarfile.getmembers():
            yield TarInode(tarinfo)

    def __getitem__(self, path):
        return TarInode(self._tarfile.getmember(path))

    def _as_tarinfo(self, item):
        ti = tarfile.TarInfo(item.path)
        ti.uid = 0
        ti.gid = 0
        ti.mode = item.mode
        ti.size = item.size
        if item.is_symlink():
            ti.type = tarfile.SYMTYPE
        elif item.is_dir():
            ti.type = tarfile.DIRTYPE
        else:
            ti.type = tarfile.REGTYPE
        return ti

    def add(self, item, fileobj=None):
        taritem = self._as_tarinfo(item)
        self._tarfile.addfile(taritem, fileobj)

    @contextmanager
    def read(self, item):
        fileobj = None
        try:
            fileobj = self._tarfile.extractfile(item.path)
            yield fileobj
        finally:
            if fileobj is not None:
                fileobj.close()

    def close(self):
        self._tarfile.close()


class TarInode(Inode):
    def __init__(self, tarinfo):
        self._tarinfo = tarinfo

    def is_dir(self):
        return self._tarinfo.isdir()

    def is_file(self):
        return self._tarinfo.isfile()

    def is_symlink(self):
        return self._tarinfo.issym()

    @property
    def mode(self):
        return self._tarinfo.mode

    @property
    def path(self):
        return self._tarinfo.name

    @property
    def size(self):
        return self._tarinfo.size

    @property
    def type(self):
        return self._tarinfo.type
