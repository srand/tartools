import argparse
import hashlib
import io
import os
import pathlib
import sys

from tartools.directory import DirectoryTree
from tartools.tar import TarTree


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


def checksum(source, hashfn):
    source = new_tree(source)

    for inode in source:
        if not inode.is_file():
            continue
        print(source.checksum(inode, hashfn), "", inode.path)

    source.close()


def checksum_check(source, hashfn, check_path):
    source = new_tree(source)

    delta = False
    with open(check_path) as check_file:
        for line in check_file:
            checksum, filepath = line.split("  ", 1)
            checksum, filepath = checksum.strip(), filepath.strip()
            try:
                inode = source[filepath]
                if not inode.is_file():
                    continue
                if source.checksum(inode, hashfn) != checksum:
                    delta = True
                    print(inode.path, "differs")
            except KeyError:
                delta = True
                print(filepath, "missing")

    source.close()
    return not delta


def main():
    parser = argparse.ArgumentParser(
        description='Checksum tar archives or directory trees.')
    parser.add_argument(
        'source', type=pathlib.Path, help='first tar archive or directory')
    algos = parser.add_mutually_exclusive_group()
    algos.add_argument(
        '--md5', action="store_true", help='use md5')
    algos.add_argument(
        '--sha1', action="store_true", help='use sha1')
    algos.add_argument(
        '--sha256', action="store_true", help='use sha256')
    parser.add_argument(
        '-c', '--check', type=pathlib.Path, help='read checksums from file and check them')
    args = parser.parse_args()

    hashfn = hashlib.sha1
    if args.md5:
        hashfn = hashlib.md5
    if args.sha1:
        hashfn = hashlib.sha1
    if args.sha256:
        hashfn = hashlib.sha256

    if args.check:
        sys.exit(0 if checksum_check(args.source, hashfn, args.check) else -1)
    else:
        checksum(args.source, hashfn)


if __name__ == "__main__":
    main()
