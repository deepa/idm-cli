""" Copyright 2017 Akamai Technologies, Inc. All Rights Reserved.
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

import json


class identityManagement(object):
    def __init__(self, access_hostname):
        self.access_hostname = access_hostname

    def list_account_switch_keys(self, session, openIdentitiyId, search=None):
        """
        Function to list available contexts for managing accounts
        
        Arguments:
            openIdentityId {str} -- A unique identifier for each API client
            search {str} -- An optional search key to filter the contexts
            session {Session} -- An EdgeGrid Auth akamai session object
        
        Returns:
            Response -- Object containing the response details
        """

        list_contexts_url = 'https://' + self.access_hostname + \
            '/identity-management/v1/open-identities/' + \
            openIdentitiyId + '/account-switch-keys'
        
        if search:
            list_contexts_url = list_contexts_url + '?search=' + search

        list_contexts_response = session.get(list_contexts_url)
    
        return list_contexts_response

    def list_credentials(self, session, openIdentityId, actions=False):
        """Function to list all credentials for this client
        
        Arguments:
            openIdentityId {str} -- A unique identifier for each API client
            session {Session} -- An EdgeGrid Auth akamai session object

        Keyword Arguments:
            actions {bool} -- True to get the actions that can be performed on this credential (default: {False})
        
        Returns:
            Response -- Object containing the response details
        """

        url = 'https://' + self.access_hostname + \
            '/identity-management/v1/open-identities/' + \
            openIdentityId + '/credentials'

        if actions:
            url = url + '?actions=true'

        response = session.get(url)
    
        return response

    def get_credential(self, session, openIdentityId, credentialId, actions=False):
        """
        Function to get a single credential identified by credentialId
        
        Arguments:
            openIdentityId {str} -- A unique identifier for each API client
            actions {bool} -- True to get the actions that can be performed on this credential
            session {Session} -- An EdgeGrid Auth akamai session object
            credentialId -- Identifier for the credential retrieved by this function
        
        Keyword Arguments:
            actions {bool} -- True to get the actions that can be performed on this credential (default: {False})

        Returns:
            Response -- Object containing the response details
        """

        url = 'https://' + self.access_hostname + \
            '/identity-management/v1/open-identities/' + \
            openIdentityId + '/credentials/' + credentialId 

        if actions:
            url = url + '?actions=true'

        response = session.get(url)
        return response
    
    def get_client(self, session, accessToken, actions=False):
        """Function to list all credentials for this client
        
        Arguments:
            accessToken {str} -- An access token identifies a collection of APIs belonging to an API client
            session {Session} -- An EdgeGrid Auth akamai session object

        Keyword Arguments:
            actions {bool} -- True to get the actions that can be performed on this client (default: {False})
        
        Returns:
            Response -- Object containing the response details
        """

        url = 'https://' + self.access_hostname + \
            '/identity-management/v1/open-identities/tokens/' + accessToken

        if actions:
            url = url + '?actions=true'

        response = session.get(url)
    
        return response



    