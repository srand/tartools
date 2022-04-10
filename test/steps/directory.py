import shutil
import tempfile

from behave import given, when, then, fixture


@fixture
def workspace(context, **kwargs):
    context.workspace = tempfile.mkdtemp("behave")
    try:
        yield pathlib.Path(context.workspace)
    finally:
        shutil.rmtree(context.workspace)


@given('a directory {path}')
def step_impl(context, path):
    print(context, path)


@when('we diff {path1} {path2} into {out}')
def step_impl(context, path1, path2, out):
    pass


@then('{path} is empty')
def step_impl(context, path):
    pass
