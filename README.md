# Security-TXT
Security-TXT is a simple security.txt library.
```Python
>>> from securitytxt import SecurityTXT
>>> sec = SecurityTXT.from_url("adobe.com")
>>> sec.contact
['https://hackerone.com/adobe', 'mailto:psirt@adobe.com']
>>> sec.signature
'iQIzBAEBCAAdFiEEqvs1Pw7pNc/gvcvRX9Oj3XV3pEYFAmEBhSgACgk...'
>>> sec.expired
False
```
Security-TXT allows you to easily retrieve, parse and manipulate security.txt files. It tries to follow the latest 
[draft RFC](https://datatracker.ietf.org/doc/html/draft-foudil-securitytxt-12) as closely as possible, while it still 
parses security.txt files that contain minor mistakes. The package aims to be well-documented, thereby easy to use in 
combination with `pydoc`.

## Installation
Security-TXT is available on PyPI:
```
$ python -m pip install wellknown-securitytxt
```
The package has only been tested with Python 3.6.8+

## Supported Features & Best–Practices
The package has been build to support easy and automated retrieval and parsing of security.txt files. Therefore,
features include:
* Automated searching for security.txt files on specified host.
* Signature parsing for signed files.
* Allows for parsing unknown fields and comments that are present in security.txt file.
* Automated validity tests for parsed security.txt files.
* Every class and function is fully documented.

Soon to be implemented:
* `fail_silently`: if a file format is invalid, it continues parsing the rest of the line instead of raising an error.
