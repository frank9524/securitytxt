import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wellknown-securitytxt",
    version="0.9.7",
    author="fwesters",
    description="A package for finding and parsing security.txt files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fwesters/securitytxt",
    project_urls={
        "Source": 'https://github.com/fwesters/securitytxt',
        "Bug Tracker": "https://github.com/fwesters/securitytxt/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=['requests', 'python-dateutil'],
)
