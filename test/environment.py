from behave import fixture, use_fixture

import pathlib
import shutil
import tempfile


def before_scenario(context, feature):
    context.workspace = pathlib.Path(tempfile.mkdtemp("behave"))


def after_scenario(context, feature):
    shutil.rmtree(context.workspace)
