#!/usr/bin/env python3

# Copyright 2019 Contributors to Hyperledger Sawtooth
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------
import os
import sys
import json
import requests
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.level = logging.DEBUG
LOGGER.addHandler(logging.StreamHandler(sys.stdout))


def test_endpoint():
    """Add various demo data to suit the needs of our presenation and testing."""
    host = input("What is the hostname you would like to populate test "
                 "data to? Press enter for localhost: ")
    if host == "":
       host = "localhost"

    LOGGER.info('Starting requests')

    try:
        with requests.Session() as s:
            ["name", "username", "password", "email"]
            create = {"name": "nadia", "password": "test111", "username": "nadia", "email": "nadia@dev9.com", "auth_source": "next"}
            LOGGER.info(create)
            response = s.post('http://' + host + ':8000/api/users/', json=create)
            LOGGER.info(response)
            LOGGER.info(response.json())

            query_payload = {
                "query": {
                    "search_input": {
                        "value": "Brian Jo",
                        "fields": [
                            "email",
                            "name"
                        ]
                    },
                    "search_object_types": [
                        "user"
                    ],
                    "page_size": "20",
                    "page": "1",
                    "sort": {
                          "fields":[
                                "email",
                                "name"
                          ],
                          "order": "asc"
                    }
                }
            }
            LOGGER.info(query_payload)

            response3 = s.get('http://' + host + ':8000/api/search', json=query_payload)

            LOGGER.info(response3)
            LOGGER.info(response3.json())
    except (KeyError, IndexError):
        LOGGER.info('***************** unable to add request ^')

if __name__ == "__main__":
    test_endpoint()