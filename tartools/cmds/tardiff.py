import argparse
import io
import os
import pathlib

from tartools.directory import DirectoryTree
from tartools.tar import TarTree
from tartools.version import __version__


def new_tree(path, writeable=False):
    if path.suffixes == [".tar"]:
        return TarTree(path, "r" if not writeable else "w")
    elif path.suffixes in [[".tar", ".gz"], [".tgz"]]:
        return TarTree(path, "r:gz" if not writeable else "w:gz")
    elif path.suffixes in [[".tar", ".bz2"]]:
        return TarTree(path, "r:bz2" if not writeable else "w:bz2")
    elif path.suffixes in [[".tar", ".xz"]]:
        return TarTree(path, "r:xz" if not writeable else "w:xz")
    return DirectoryTree(path, writeable)


def pathiter(path, skip=0):
    genpath = ""
    for component in path.split(os.sep)[:-skip]:
        genpath = os.path.join(genpath, component)
        yield genpath


def new_diff():
    pass


def diff(source1, source2, diffout, bsdiff=False):
    source1 = new_tree(source1)
    source2 = new_tree(source2)
    diffout = new_tree(diffout, writeable=True)

    if bsdiff:
        import bsdiff4

    deleted = []

    def is_deleted(inode):
        for d in deleted:
            if d.is_parent_of(inode.path):
                return True
        return False

    for inode1 in source1:
        try:
            inode2 = source2[inode1.path]
            if inode1.size != inode2.size or inode1.mode != inode2.mode:
                file2 = None
                if inode2.is_file():
                    with source2.read(inode2) as file2:
                        diffout.add(inode2, file2)
                continue

            if not inode1.is_file():
                continue

            if source1.checksum(inode1) != source2.checksum(inode2):
                with source2.read(inode2) as file2:
                    for path in pathiter(inode2.path, skip=1):
                        try:
                            diffout[path]
                        except KeyError:
                            diffout.add(source2[path])
                    if bsdiff:
                        with source1.read(inode1) as file1, source2.read(inode2) as file2:
                            diff = bsdiff4.diff(file1.read(), file2.read())
                        inode2.size = len(diff)
                        diffout.add(inode2, io.BytesIO(diff))
                    else:
                        diffout.add(inode2, file2)
        except KeyError:
            if is_deleted(inode1):
                continue
            skip = False
            for path in pathiter(inode1.path, skip=1):
                try:
                    comp = diffout[path]
                    if comp.is_whiteout():
                        skip = True
                except KeyError:
                    diffout.add(source1[path])
            if not skip:
                diffout.add_whiteout(inode1)
                deleted.append(inode1)

    for inode2 in source2:
        try:
            source1[inode2.path]
        except KeyError:
            diffout.add(inode2)

    source1.close()
    source2.close()
    diffout.close()


def main():
    parser = argparse.ArgumentParser(
        description='Diff tar archives or directory trees.')
    parser.add_argument(
        '--version', action="version", version=f"tardiff, version {__version__}")
    parser.add_argument(
        'source1', type=pathlib.Path, help='first tar archive or directory')
    parser.add_argument(
        'source2', type=pathlib.Path, help='second tar archive or directory')
    parser.add_argument(
        'diff', type=pathlib.Path, help='output diff to archive or directory')
    parser.add_argument(
        '--bsdiff', action="store_true", help='use bsdiff')
    args = parser.parse_args()
    diff(args.source1, args.source2, args.diff, args.bsdiff)


if __name__ == "__main__":
    main()
