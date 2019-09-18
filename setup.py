from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="duck",
    version="0.1",
    description="Python package facilitating duck typing"
    " through attribute traverse utilities",
    long_description=readme(),
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="decorator duck typing ducktyping wrapper utility",
    url="http://github.com/monomonedula/duck",
    author="Vladyslav Halchenko",
    author_email="valh@tuta.io",
    license="MIT",
    packages=["duck"],
    install_requires=["markdown"],
    test_suite="nose.collector",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
