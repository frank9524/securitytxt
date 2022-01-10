import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="security-txt",
    version="0.1",
    author="fwesters",
    description="A package for finding and parsing security.txt files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fwesters/security-txt",
    project_urls={
        "Source": 'https://github.com/fwesters/securitytxt',
        "Bug Tracker": "https://github.com/fwesters/securitytxt/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    package_dir={"": "securitytxt"},
    packages=setuptools.find_packages(where="securitytxt"),
    python_requires=">=3.6",
)