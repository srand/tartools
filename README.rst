tartools
========

tartools provide utilities for comparing and patching tar archives and filesystem trees.


tardiff
-------

Tardiff is a command line utility that compares tar archives to other tar archives or filesystem trees and produces a new archive with the delta.

The delta archive can be used when building a Docker image to reproduce the second archive from the first.

  .. code:: bash

     $ tardiff alpine3.14.tar alpine3.15.tar delta.tar

  .. code:: Dockerfile

     FROM alpine:3.14
     ADD delta.tar /
     # Rootfs is now equal to alpine:3.15


Optionally, tardiff can also be run in bsdiff mode where minimal binary diffs are stored in the delta archive instead of entire files. This reduces size significantly at the cost of speed. The delta archive must be re-applied with the tarapply tool.

tarsum
------

tarsum checksums and outputs digests of files in an archive or a directory.

  .. code:: bash

     $ tarsum archive.tar

     $ tarsum --md5 archive.tgz

     $ tarsum --sha1 archive.tar.bz2

     $ tarsum --sha256 archive-tree/
