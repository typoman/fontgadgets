from setuptools import setup, find_packages

setup(
    name="fontGadgets",
    version="0.0.1",
    description="A package to add more functions to fontParts and defcon",
    author="Bahman Eslami",
    author_email="contact@bahman.design",
    url="http://bahman.design",
    license="MIT",
    platforms=["Any"],
    package_dir={'': 'Lib'},
    packages=find_packages('Lib'),
    install_requires=[
    "fontParts",
    "defcon",
    "fontTools",
    "ufo2ft",
    "ufoLib2",
    "pytest",
    "ufonormalizer",
    "fontGit",
    "python-bidi==0.4.2",  # pin for now, 0.5 breaks things
    "fontTools==4.55.2",
    "uharfbuzz==0.45.0",
    ],
    tests_require=[
        'pytest>=3.9',
    ],
)
