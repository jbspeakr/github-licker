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
from collections import namedtuple

import urllib.request
import json

Repositories = namedtuple('Repositories', ['with_license', 'without_license'])


class Licker(object):

    def __init__(self, organisation, token):
        self.api = 'https://api.github.com'
        self.repository_url = '%s/orgs/%s/repos?type=all' % (self.api, organisation)
        self.license_url = '%s/repos/%s/' % (self.api, organisation)
        self.page_parameter = '&page='

        self.request_headers = {
            'Authorization': 'token %s' % token,
            'Accept': 'application/vnd.github.drax-preview+json'}

    def _fetch_repositories(self):
        page_number = 1
        repositories = []
        json_response = []

        print('start connecting to github...')
        while json_response or page_number == 1:
            request = urllib.request.Request(
                url='%s%s%s' % (self.repository_url, self.page_parameter, page_number),
                headers=self.request_headers)

            if page_number == 1:
                print('start collecting repositories...')

            response = urllib.request.urlopen(request).read()
            json_response = json.loads(response.decode('utf-8'))
            repositories.extend(json_response)

            page_number += 1

        return repositories

    def _fetch_license_information(self, repositories):
        repos_with_license = []
        repos_without_license = []

        print('start fetching license information...')
        for repository in repositories:
            if not repository['fork']:
                request = urllib.request.Request(
                    url=self.license_url + repository['name'],
                    headers=self.request_headers)

                response = urllib.request.urlopen(request).read()
                json_response = json.loads(response.decode('utf-8'))

                if json_response['license']:
                    repos_with_license.append({
                        'name': repository['name'],
                        'license': json_response['license']['name']})
                else:
                    repos_without_license.append(repository['name'])

        return Repositories(repos_with_license, repos_without_license)

    def run_license_analysis(self):
        repositories = self._fetch_repositories()
        repos = self._fetch_license_information(repositories)

        if repos.with_license:
            print('\nfound %s repositories with license:\n' % len(repos.with_license))
            for repository in repos.with_license:
                print('\t%s -- %s' % (repository['name'], repository['license']))

        if repos.without_license:
            print('\nfound %s repositories without license:\n' % len(repos.without_license))
            for repository in repos.without_license:
                print('\t%s' % repository)
