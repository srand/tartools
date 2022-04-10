tartools
========

tartools provide utilities for comparing and patching tar archives and filesystem trees.


tardiff
-------

Tardiff compares tar archives to other tar archives and produces a new archive with the delta. In addition to archives, the command also works on directory trees and any combination of the two. Common compression formats are also supported.

The delta archive can be used when building a Docker image to reproduce the second archive from the first.

  .. code:: bash

     $ tardiff alpine3.14.tar alpine3.15.tar delta.tar

     $ tardiff alpine3.14.tar.gz alpine3.15.tar.xz delta/

     $ tardiff alpine3.14/ alpine3.15/ delta.tar.bz2

  .. code:: Dockerfile

     FROM alpine:3.14
     ADD delta.tar /
     # Rootfs is now equal to alpine:3.15


Optionally, tardiff can also be run in bsdiff mode where minimal binary diffs are stored in the delta archive instead of entire files. This reduces size significantly at the cost of speed. The delta archive must be re-applied with the tarapply tool.

  .. code:: bash

     $ tardiff --bsdiff alpine3.14.tar alpine3.15.tar delta.tar


tarapply
--------

Tarapply takes a delta diff archive and patches the original archive to produce a new archive. Like tardiff, directory trees are also supported as well as archive compression.

  .. code:: bash

     $ tarapply alpine3.14.tar delta.tar alpine3.15.tar

     $ tarapply --bsdiff alpine3.14/ delta.tar alpine3.15/


tarsum
------

tarsum checksums and outputs digests of files in an archive or a directory.

  .. code:: bash

     $ tarsum archive.tar

     $ tarsum --md5 archive.tgz

     $ tarsum --sha1 archive.tar.bz2

     $ tarsum --sha256 archive-tree/
