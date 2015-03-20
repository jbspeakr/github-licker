#!/usr/bin/env python
# Licker - Github License Checker for Organisational Repositories
# Copyright 2015 Jan Brennenstuhl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
usage:
    licker.py [TOKEN] [options]

options:
    -o, --organisation=ORGANISATION  the Github organisation you want to check [default: ImmobilienScout24]
"""

import urllib.request
import json

from docopt import docopt


def run():
    arguments = docopt(__doc__)
    organisation = arguments["--organisation"]
    token = arguments['TOKEN']

    if not token:
        with open('GITHUB_TOKEN', 'r') as fd:
            token = fd.readline().strip()  # Can't hurt to be paranoid

    api = 'https://api.github.com'
    repository_url = '%s/orgs/%s/repos?type=all' % (api, organisation)
    license_url = '%s/repos/%s/' % (api, organisation)
    page_parameter = '&page='

    request_headers = {
        'Authorization': 'token %s' % token,
        'Accept': 'application/vnd.github.drax-preview+json'}

    json_response = repositories = []
    page_number = 1

    print('start connecting to github...')
    while json_response or page_number == 1:
        request = urllib.request.Request(
            url='%s%s%s' % (repository_url, page_parameter, page_number),
            headers=request_headers)

        if page_number == 1:
            print('start collecting repositories...')

        response = urllib.request.urlopen(request).read()
        json_response = json.loads(response.decode('utf-8'))
        repositories.extend(json_response)

        page_number += 1

    repos_with_license = []
    repos_without_license = []

    print('start fetching license information...')
    for repository in repositories:
        if not repository['fork']:
            request = urllib.request.Request(
                url=license_url + repository['name'],
                headers=request_headers)

            response = urllib.request.urlopen(request).read()
            json_response = json.loads(response.decode('utf-8'))

            if json_response['license']:
                repos_with_license.append({
                    'name': repository['name'],
                    'license': json_response['license']['name']})
            else:
                repos_without_license.append(repository['name'])
                # print('\t%s -- %s' % (repository['name'], 'NO LICENSE'))

    if repos_with_license:
        print('\nfound %s repositories with license:\n' % len(repos_with_license))
        for repository in repos_with_license:
            print('\t%s -- %s' % (repository['name'], repository['license']))

    if repos_without_license:
        print('\nfound %s repositories without license:\n' % len(repos_without_license))
        for repository in repos_without_license:
            print('\t%s' % repository)


if __name__ == "__main__":
    run()




