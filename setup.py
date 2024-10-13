from setuptools import setup, find_packages
import sys

sys.path.append("./test/")
version = "1.0.4"

setup(
    name="dlchordx",
    version=version,
    description="chord library",
    author="anime-song",
    url="https://github.com/anime-song/DLChordX",
    keywords='music chord',
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    test_suite='test',
)
