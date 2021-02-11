import setuptools

With open("README.md", "r" as fh:
    long_description = fh.read()

setuptools.setup(
    name="cgli",
    version="0.0.1",
    author="Toni Cornelissen",
    author_email="cgli@technetium.be",
    description="utility to execute a pythonscript from both commandline and webserver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/technetium/cgli/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU :: GPL :: 3.0"
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)   
    