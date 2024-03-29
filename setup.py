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
    "fontTools",
    "ufo2ft",
    "ufoLib2",
    "pytest",
    "ufonormalizer"
    ],
    tests_require=[
        'pytest>=3.7',
    ],
)
