"""
Copyright 2017 Akamai Technologies, Inc. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

"""
This code leverages akamai OPEN API. to control Certificates deployed in Akamai Network.
In case you need quick explanation contact the initiators.
Initiators: dthiagar@akamai.com, rpunjabi@akamai.com
"""

import json
from iamwrapper import identityManagement
import argparse
import requests
import os
import configparser
import logging
import sys
from prettytable import PrettyTable
from akamai.edgegrid import EdgeGridAuth, EdgeRc
import datetime


PACKAGE_VERSION = "0.1.0"

# Setup logging
if not os.path.exists('logs'):
    os.makedirs('logs')
log_file = os.path.join('logs', 'akamai-iam.log')

# Set the format of logging in console and file separately
log_formatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
console_formatter = logging.Formatter("%(message)s")
root_logger = logging.getLogger()

logfile_handler = logging.FileHandler(log_file, mode='w')
logfile_handler.setFormatter(log_formatter)
root_logger.addHandler(logfile_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(console_formatter)
root_logger.addHandler(console_handler)
# Set Log Level to DEBUG, INFO, WARNING, ERROR, CRITICAL
root_logger.setLevel(logging.INFO)


def init_config(edgerc_file, section):
    if not edgerc_file:
        if not os.getenv("AKAMAI_EDGERC"):
            edgerc_file = os.path.join(os.path.expanduser("~"), '.edgerc')
        else:
            edgerc_file = os.getenv("AKAMAI_EDGERC")

    if not os.access(edgerc_file, os.R_OK):
        root_logger.error("Unable to read edgerc file \"%s\"" % edgerc_file)
        exit(1)

    if not section:
        if not os.getenv("AKAMAI_EDGERC_SECTION"):
            section = "iam"
        else:
            section = os.getenv("AKAMAI_EDGERC_SECTION")

    try:
        edgerc = EdgeRc(edgerc_file)
        base_url = edgerc.get(section, 'host')
        access_token = edgerc.get(section, 'access_token')

        session = requests.Session()
        session.auth = EdgeGridAuth.from_edgerc(edgerc, section)

        return base_url, session, access_token
    except configparser.NoSectionError:
        root_logger.error("Edgerc section \"%s\" not found" % section)
        exit(1)
    except Exception:
        root_logger.info(
            "Unknown error occurred trying to read edgerc file (%s)" %
            edgerc_file)
        exit(1)

def cli():
    prog = get_prog_name()
    if len(sys.argv) == 1:
        prog += " [command]"

    parser = argparse.ArgumentParser(
        description='Akamai CLI for IAM',
        add_help=False,
        prog=prog)
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s ' +
                PACKAGE_VERSION)

    subparsers = parser.add_subparsers(
        title='Commands', dest="command", metavar="")

    actions = {}

    subparsers.add_parser(
        name="help",
        help="Show available help",
        add_help=False).add_argument(
        'args',
        metavar="",
        nargs=argparse.REMAINDER)

    actions["list_account_switch_keys"] = create_sub_command(
        subparsers, "list-account-switch-keys", "List the accountSwitchKeys and account names you can access based on the permissions of your API client",
        [{"name": "search", "help": "Use this to filter results by accountId or accountName. Enter at least three characters in the string to filter the results."},
        {"name": "json", "help": "output format in json"}],
        [{"name": "open-identity-id", "help": "A unique identifier for each API client"}])

    actions["list_credentials"] = create_sub_command(
        subparsers, "list-credentials", "Get an API client’s credentials",
        [{"name": "actions", "help": "Include to get the actions that can be preformed on this credential", "action":"store_true"}],
        [{"name": "open-identity-id", "help": "A unique identifier for each API client"}])

    actions["get_credential"] = create_sub_command(
        subparsers, "get-credential", "Get details for a single credential",
        [{"name": "actions", "help": "Optionally enable actions to include them as part of the response object", "action":"store_true"}],
        [{"name": "open-identity-id", "help": "A unique identifier for each API client"}, {"name": "credential-id", "help": "A credential’s unique identifier"}])

    actions["get_client"] = create_sub_command(
        subparsers, "get-client", "View an API client’s details",
        [{"name": "actions", "help": "Include to get the actions that can be preformed on this credential", "action":"store_true"},
        {"name": "access-token", "help": "An access token identifies a collection of APIs belonging to an API client"}])

    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        return 0

    if args.command == "help":
        if len(args.args) > 0:
            if actions[args.args[0]]:
                actions[args.args[0]].print_help()
        else:
            parser.prog = get_prog_name() + " help [command]"
            parser.print_help()
        return 0

    # Override log level if user wants to run in debug mode
    # Set Log Level to DEBUG, INFO, WARNING, ERROR, CRITICAL
    if args.debug:
        root_logger.setLevel(logging.DEBUG)

    return getattr(sys.modules[__name__], args.command.replace("-", "_"))(args)


def create_sub_command(
        subparsers,
        name,
        help,
        optional_arguments=None,
        required_arguments=None):
    action = subparsers.add_parser(name=name, help=help, add_help=False)

    if required_arguments:
        required = action.add_argument_group("required arguments")
        for arg in required_arguments:
            name = arg["name"]
            del arg["name"]
            required.add_argument("--" + name,
                                  required=True,
                                  **arg,
                                  )

    optional = action.add_argument_group("optional arguments")
    if optional_arguments:
        for arg in optional_arguments:
            name = arg["name"]
            del arg["name"]
            if name == 'force' or name == 'json':
                optional.add_argument(
                    "--" + name,
                    required=False,
                    **arg,
                    action="store_true")
            else:
                optional.add_argument("--" + name,
                                      required=False,
                                      **arg,
                                      )
            
    optional.add_argument(
        "--edgerc",
        help="Location of the credentials file [$AKAMAI_EDGERC]",
        default=os.path.join(
            os.path.expanduser("~"),
            '.edgerc'))

    optional.add_argument(
        "--section",
        help="Section of the credentials file [$AKAMAI_EDGERC_SECTION]",
        default="iam")

    optional.add_argument(
        "--debug",
        help="DEBUG mode to generate additional logs for troubleshooting",
        action="store_true")

    return action


def list_credentials(args):
    base_url, session = init_config(args.edgerc, args.section)
    identityManagementObject = identityManagement(base_url)
    response = identityManagementObject.list_credentials(session, args.open_identity_id, args.actions)

    if response.status_code == 200:
        root_logger.info(json.dumps(response.json(), indent=4))
    else:
        root_logger.info(
            'There was error in fetching response. Use --debug for more information.')
        root_logger.debug(json.dumps(response.json(), indent=4))


def list_account_switch_keys(args):
    base_url, session = init_config(args.edgerc, args.section)
    identityManagementObject = identityManagement(base_url)
    response = identityManagementObject.list_account_switch_keys(session, args.open_identity_id, args.search)

    if response.status_code == 200:

        if args.json:
            root_logger.info(json.dumps(response.json(), indent=4))
            return

        table = PrettyTable(['accountSwitchKey', 'Account Name'])
        table.align = "l"

        for eachItem in response.json():
            rowData = []
            accountSwitchKey = eachItem['accountSwitchKey']
            accountName = eachItem['accountName']
            
            rowData.append(accountSwitchKey)
            rowData.append(accountName)

            table.add_row(rowData)
        root_logger.info(table)
    else:
        root_logger.info(
            'There was error in fetching response. Use --debug for more information.')
        root_logger.debug(json.dumps(response.json(), indent=4))


def get_credential(args):
    base_url, session = init_config(args.edgerc, args.section)
    identityManagementObject = identityManagement(base_url)
    response = identityManagementObject.get_credential(session, args.open_identity_id, args.credential_id, args.actions)

    if response.status_code != 200:
        root_logger.info(
            'There was error in fetching response. Use --debug for more information.')

    root_logger.info(json.dumps(response.json(), indent=4))


def get_client(args):
    base_url, session, access_token = init_config(args.edgerc, args.section)
    identityManagementObject = identityManagement(base_url)

    if args.access_token: 
        response = identityManagementObject.get_client(session, args.access_token, args.actions)
    else:
        response = identityManagementObject.get_client(session, access_token, args.actions)

    if response.status_code == 200:
        root_logger.info(json.dumps(response.json(), indent=4))
    else:
        root_logger.info(
            'There was error in fetching response. Use --debug for more information.')
        root_logger.debug(json.dumps(response.json(), indent=4))

def get_prog_name():
    prog = os.path.basename(sys.argv[0])
    if os.getenv("AKAMAI_CLI"):
        prog = "akamai iam"
    return prog


def get_cache_dir():
    if os.getenv("AKAMAI_CLI_CACHE_DIR"):
        return os.getenv("AKAMAI_CLI_CACHE_DIR")

    return os.curdir


# Final or common Successful exit
if __name__ == '__main__':
    try:
        status = cli()
        exit(status)
    except KeyboardInterrupt:
        exit(1)
