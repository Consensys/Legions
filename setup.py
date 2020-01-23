from setuptools import setup, find_packages
from setuptools.command.install import install
import sys
import os

from legions.version import __version__


def read_file(fname):
    """
    return file contents
    :param fname: path relative to setup.py
    :return: file contents
    """
    with open(os.path.join(os.path.dirname(__file__), fname), "r") as fd:
        return fd.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""

    description = "verify that the git tag matches our version"

    def run(self):
        tag = os.getenv("CIRCLE_TAG")

        if tag != __version__:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, __version__
            )
            sys.exit(info)


setup(
    name="legions",
    version=__version__,
    # description="Handy toolkit for (security) researchers poking around Ethereum nodes and contracts, now with a slick command-line interface, with auto complete commands and history.",
    long_description=read_file("Readme.md") if os.path.isfile("Readme.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/consensys/Legions",
    author="Shayan Eskandari - ConsenSys Diligence",
    author_email="shayan.eskandari@consensys.net",
    license="MIT",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    package_data={"legions": ["commands/**"],},
    install_requires=read_file("requirements.txt").split("\n"),
    entry_points="""
          [console_scripts]
          legions=legions.main:main
      """,
    cmdclass={"verify": VerifyVersionCommand},
    zip_safe=False,
)
