from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="MDBDict",
    version="1.0.4",
    description="A wrapper for Pymongo that turns clusters into auto-updating dictionaries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/trigtbh/mdbdict",
    author="trigtbh",
    author_email="python.trig@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Database"
    ],
    keywords="mongodb, pymongo, dictionary",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=["pymongo"],
)