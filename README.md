# Github Licker
[![Build Status](https://travis-ci.org/jbspeakr/github-licker.svg?branch=master)](https://travis-ci.org/jbspeakr/github-licker)
[![Codacy Badge](https://www.codacy.com/project/badge/8392a84f11634b27a985b334d56ab089)](https://www.codacy.com/public/jan_1691/github-licker)

**Licker - Your Github License Checker for Organisational Repositories.**

Using the [Github API v3](https://developer.github.com/v3/) including the [Licenses API](https://developer.github.com/v3/licenses/) developer preview, 
Licker is able to check licenses of all repositories in your Github organisation. It helps especially identifying repos 
without license file.

## Prerequisites
- Python 3
- [Github Token](https://github.com/blog/1509-personal-api-tokens) for increasing the unauthenticated rate limit (Optional)

## How-To
```
usage:
    licker [TOKEN] [options]

options:
    -o, --organisation=ORGANISATION  the Github organisation you want to check [default: ImmobilienScout24]
```

## License
Monocyte is licensed under [Apache License, Version 2.0](https://github.com/ImmobilienScout24/aws-monocyte/blob/master/LICENSE.txt).


