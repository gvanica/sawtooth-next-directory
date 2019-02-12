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
from sanic import Blueprint
from sanic.response import json

from rbac.common.logs import get_logger
from rbac.server.api.auth import authorized
from rbac.server.db import db_utils
from rbac.server.db.roles_query import roles_search_name
from rbac.server.db import users_query

LOGGER = get_logger(__name__)
SEARCH_BP = Blueprint("search")


@SEARCH_BP.post("api/search")
@authorized()
async def search_all(request):
    """API Endpoint to get all roles, packs, or users containing a string."""
    search_query = request.json.get("query")

    # Check for valid payload containing query and search object types
    if search_query is None:
        errors = {"errors": "No query parameter recieved."}
        return json(errors)
    if "search_object_types" not in search_query:
        errors = {"errors": "No search_object_types for search recieved."}
        return json(errors)
    if "search_input" not in search_query:
        errors = {"errors": "No search_input string for search recieved."}
        return json(errors)

    # Create resopnse data object
    respdata = {"packs": [], "roles": [], "users": []}

    if "pack" in search_query["search_object_types"]:
        # Fetch packs with search input string
        pack_results = []  # Future pack query issue #1176
        respdata["packs"] = pack_results

    if "role" in search_query["search_object_types"]:
        # Fetch roles with search input string
        role_results = []
        respdata["roles"] = role_results

    if "user" in search_query["search_object_types"]:
        # Fetch users with search input string
        user_results = await search_users(request, search_query)  # Future user query issue #1175
        respdata["users"] = user_results

    #data = sort_and_paginate(search_query, data)

    return json({"data": respdata})


def sort_and_paginate(search_query, data):
    """Sort response and paginate the result"""
    return data


async def search_users(request, search_query):
    """Function to search for roles"""

    conn = await db_utils.create_connection(
        request.app.config.DB_HOST,
        request.app.config.DB_PORT,
        request.app.config.DB_NAME,
    )

    search_input_value = search_query["search_input"]["value"]
    search_input_fields = search_query["search_input"]["fields"]

    search_input_value = "Brian Jo"
    LOGGER.info("before calling db")
    result = await users_query.search_users_db(conn, search_input_value, search_input_fields)

    conn.close()

    return json(result)
