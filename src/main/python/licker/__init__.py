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
import logging

from collections import namedtuple
from urllib.error import HTTPError
from urllib.request import Request

Repositories = namedtuple('Repositories', ['with_license', 'without_license'])


class LicenseChecker(object):

    def __init__(self, organisation, token):
        self.api = 'https://api.github.com'
        self.repository_url = '%s/orgs/%s/repos?type=all' % (self.api, organisation)
        self.license_url = '%s/repos/%s/' % (self.api, organisation)
        self.page_parameter = '&page='
        self.request_headers = {
            'Accept': 'application/vnd.github.drax-preview+json'  # Required for developer preview
        }

        if token:
            self.request_headers['Authorization'] = 'token %s' % token

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

    def _fetch_repositories(self):
        page_number = 1
        repositories = []
        json_response = []

        self.logger.info('Start connecting to Github.')
        while json_response or page_number == 1:
            request = Request(
                url='%s%s%s' % (self.repository_url, self.page_parameter, page_number),
                headers=self.request_headers)

            try:
                response = urllib.request.urlopen(request).read()
                json_response = json.loads(response.decode('utf-8'))
                repositories.extend(json_response)

                if page_number == 1:
                    self.logger.info('Start collecting repositories.')
            except HTTPError as e:
                if e.code == 401:
                    self.logger.error('Given token is not authorized.')
                else:
                    self.logger.error('Something went wrong while connecting to Github.')

            page_number += 1

        return repositories

    def _fetch_license_information(self, repositories):
        repositories_with_license = []
        repositories_without_license = []

        self.logger.info('Start fetching license information.')
        for repository in repositories:
            if not repository['fork']:
                request = urllib.request.Request(
                    url=self.license_url + repository['name'],
                    headers=self.request_headers)

                response = urllib.request.urlopen(request).read()
                json_response = json.loads(response.decode('utf-8'))

                if json_response['license']:
                    repositories_with_license.append({
                        'repo': repository['name'],
                        'license': json_response['license']['name']})
                else:
                    repositories_without_license.append({
                        'repo': repository['name'],
                        'license': 'None'})

        return Repositories(repositories_with_license, repositories_without_license)

    def run_license_analysis(self):
        all_repositories = self._fetch_repositories()

        if not all_repositories:
            self.logger.info('Found no repositories.')
            return

        non_fork_repositories = self._fetch_license_information(all_repositories)

        if non_fork_repositories.with_license:
            self.logger.info('Found %s repositories with licenses: %s' % (
                len(non_fork_repositories.with_license),
                str(non_fork_repositories.with_license)))

        if non_fork_repositories.without_license:
            self.logger.info('Found %s repositories without licenses: %s' % (
                len(non_fork_repositories.without_license),
                str(non_fork_repositories.without_license)))

        return non_fork_repositories
