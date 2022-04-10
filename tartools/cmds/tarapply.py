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


def apply(source, diff, output, bsdiff=False, whiteouts=True):
    source = new_tree(source)
    diff = new_tree(diff)
    output = new_tree(output, writeable=True)

    if bsdiff:
        import bsdiff4

    for inode1 in source:
        try:
            inode2 = diff[inode1.path]
            if inode1.is_file() and inode2.is_file() and bsdiff:
                with source.read(inode1) as file1, diff.read(inode2) as file2:
                    patched = bsdiff4.patch(file1.read(), file2.read())
                inode2.size = len(patched)
                output.add(inode2, io.BytesIO(patched))
            else:
                # print(inode1.path, "->", inode2.path)
                output.add(inode2)
        except KeyError:
            # print(inode1.path, "kept")
            if inode1.is_file():
                with source.read(inode1) as file1:
                    output.add(inode1, file1)
            else:
                output.add(inode1)

    source.close()
    diff.close()
    output.close()


def main():
    parser = argparse.ArgumentParser(
        description='Apply diff to tar archives or directory trees.')
    parser.add_argument(
        '--version', action="version", version=f"tarapply, version {__version__}")
    parser.add_argument(
        'source', type=pathlib.Path, help='source archive or directory')
    parser.add_argument(
        'diff', type=pathlib.Path, help='diff archive or directory')
    parser.add_argument(
        'output', type=pathlib.Path, help='patched output archive or directory')
    parser.add_argument(
        '--bsdiff', action="store_true", help='use bsdiff')
    parser.add_argument(
        '--no-whiteouts', action="store_true", help='ignore whiteouts')
    args = parser.parse_args()
    apply(args.source, args.diff, args.output, args.bsdiff, not args.no_whiteouts)


if __name__ == "__main__":
    main()
