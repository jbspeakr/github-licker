# Github Licker

**Licker - Your Github License Checker for Organisational Repositories.**

Using the [Github API v3](https://developer.github.com/v3/) including the [Licenses API](https://developer.github.com/v3/licenses/) developer preview, 
Licker is able to check licenses of all repositories in your Github organisation. It helps especially identifying repos 
without license file.

**For more info, read my blog post: [Github-Licker - A Github License Checker](https://www.janbrennenstuhl.eu/github-license-checker/).**

## Prerequisites
- Python 3
- [Github Token](https://github.com/blog/1509-personal-api-tokens) for increasing the unauthenticated rate limit (Optional)

## How-To
```
pip install github-licker
licker -h

usage:
    licker [TOKEN] [options]

options:
    -o, --organisation=ORGANISATION  the Github organisation you want to check [default: ImmobilienScout24]
```

## License
Github Licker is licensed under [Apache License, Version 2.0](https://github.com/ImmobilienScout24/aws-monocyte/blob/master/LICENSE.txt).


