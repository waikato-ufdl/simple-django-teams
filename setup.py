from setuptools import setup, find_packages


def _read(filename: str) -> str:
    """
    Reads in the content of the file.

    :param filename:    The file to read.
    :return:            The file content.
    """
    with open(filename, "r") as file:
        return file.read()


setup(
    name="simple-django-teams",
    description="Simple Django teams.",
    long_description=f"{_read('DESCRIPTION.rst')}\n"
                     f"{_read('CHANGES.rst')}",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Programming Language :: Python :: 3.7',
    ],
    license='MIT',
    package_dir={
        '': 'src'
    },
    packages=find_packages(where="src"),
    version="0.0.3",
    author='Corey Sterling',
    author_email='coreytsterling@gmail.com',
    install_requires=[
        "django"
    ]
)
