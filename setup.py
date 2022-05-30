from setuptools import setup

setup(
    name="dweeter",
    version="0.1.0",
    description="A python module for messaging through the free dweet service.",
    long_description="https://github.com/jacklinquan/dweeter",
    long_description_content_type="text/markdown",
    url="https://github.com/jacklinquan/dweeter",
    author="Quan Lin",
    author_email="jacklinquan@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    packages=["dweeter"],
    install_requires=["cryptodweet"],
)
