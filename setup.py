"""
A setuptools based on setup module for SAND (System dAta oN Desktop)
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
    name="sand",
    version="0.1",
    description="System dAta oN Desktop",
    # The project's main homepage.
    url="https://github.com/m1ch3al/madis.git",
    # Author details
    author="Renato Sirola",
    author_email="renato.sirola@gmail.com",
    # Choose your license
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    # What does your project relate to?
    keywords="hardware sensors screen data on desktop",
    include_package_data=True,
    package_data={
        'sand': ['*/*.yaml', '*.yaml'],
        'sand.modules.cpu': ['*/*.yaml', '*.yaml', '*/*.png', '*.png'],
        'sand.modules.memory': ['*/*.yaml', '*.yaml', '*/*.png', '*.png'],
        'sand.modules.hard_drives': ['*/*.yaml', '*.yaml', '*/*.png', '*.png'],
        'sand.modules.network': ['*/*.yaml', '*.yaml', '*/*.png', '*.png'],
    },
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=[
        'setuptools',
        'PyYAML',
    ],
    packages=[
        'sand',
        'sand.modules',
        'sand.modules.cpu',
        'sand.modules.memory',
        'sand.modules.hard_drives',
        'sand.modules.network',
    ]
)


import os.path
homedir = os.path.expanduser("~")
sand_configuration_folder = os.path.join(homedir, ".sand")
os.system("mkdir {}".format(sand_configuration_folder))
os.system("cp src/sand/configuration.yaml {}".format(sand_configuration_folder))

