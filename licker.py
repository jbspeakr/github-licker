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

import urllib.request
import json

page_parameter = '&page='
api = 'https://api.github.com'
organisation = 'ImmobilienScout24'
repository_url = '%s/orgs/%s/repos?type=all' % (api, organisation)
license_url = '%s/repos/%s/' % (api, organisation)
token = ''

with open('GITHUB_TOKEN', 'r') as fd:
    token = fd.readline().strip()  # Can't hurt to be paranoid

request_headers = {
    'Authorization': 'token %s' % token,
    'Accept': 'application/vnd.github.drax-preview+json'}

json_response = repositories = []
page_number = 1

while json_response or page_number == 1:
    request = urllib.request.Request(
        url='%s%s%s' % (repository_url, page_parameter, page_number),
        headers=request_headers)

    response = urllib.request.urlopen(request).read()
    json_response = json.loads(response.decode('utf-8'))
    repositories.extend(json_response)

    page_number += 1


for repository in repositories:
    if not repository['fork']:
        request = urllib.request.Request(
            url=license_url + repository['name'],
            headers=request_headers)

        response = urllib.request.urlopen(request).read()
        json_response = json.loads(response.decode('utf-8'))

        if json_response['license']:
            print('%s -- %s' % (repository['name'], json_response['license']['name']))
        else:
            print('%s -- %s' % (repository['name'], 'NO LICENSE'))



