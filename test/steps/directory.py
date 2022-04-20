import os
import shutil
import subprocess
import tempfile

from behave import given, when, then, fixture
from tartools.cmds import tarapply, tardiff


@given('a directory {path}')
def step_impl(context, path):
    os.mkdir(context.workspace / path)


@given('a test directory {path}')
def step_impl(context, path):
    path = context.workspace / path
    os.mkdir(path)
    os.mkdir(path / "dir")

    with open(path / "file", "w") as f:
        f.write("file")

    with open(path / "dir" / "file", "w") as f:
        f.write("dir/file")

    subprocess.check_call(["ln", "-sf", "file", path / "link"])
    subprocess.check_call(["ln", "-sf", "../dir/file", path / "dir" / "link"])


@given('a file {path}')
def step_impl(context, path):
    with open(context.workspace / path, "w"):
        pass


@when('we remove {path}')
def step_impl(context, path):
    path = context.workspace / path
    try:
        shutil.rmtree(path)
    except:
        os.unlink(path)


@when('we diff {path1} and {path2} into {out}')
def step_impl(context, path1, path2, out):
    tardiff.diff(
        context.workspace / path1,
        context.workspace / path2,
        context.workspace / out)


@when('we apply {diff} to {path1} into {path2}')
def step_impl(context, diff, path1, path2):
    tarapply.apply(
        context.workspace / path1,
        context.workspace / diff,
        context.workspace / path2)


@then('{path} is empty')
def step_impl(context, path):
    path = context.workspace / path
    assert len(list(os.scandir(path))) == 0, "Files found"


@then('{path} does exists')
def step_impl(context, path):
    path = context.workspace / path
    assert path.exists(), "Files found"


@then('{path} does not exists')
def step_impl(context, path):
    path = context.workspace / path
    assert path.exists(), "Files found"


@then('directories {path1} and {path2} are identical')
def step_impl(context, path1, path2):
    subprocess.check_call(["ls", "-l", context.workspace / path1])
    subprocess.check_call(["ls", "-l", context.workspace / path2])
    subprocess.check_call(["diff", "--no-dereference", context.workspace / path1, context.workspace / path2])
