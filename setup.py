# https://www.codementor.io/@ajayagrawal295/how-to-publish-your-own-python-package-12tbhi20tf
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cgli",
    version="0.0.2",
    author="Toni Cornelissen",
    author_email="cgli@technetium.be",
    description="utility to execute a pythonscript from both commandline and webserver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/technetium/cgli/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)   

'''
python setup.py sdist bdist_wheel
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*


'''    