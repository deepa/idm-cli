# cli-idm
Provides a way to interact with Identity Management related information via Open APIs. Functionality includes viewing details about OPEN clients and credentials.

## Local Install
* Python 3+
* pip install -r requirements.txt

### Credentials

In order to use this module, you need to:

* Set up your credential files as described in the [authorization](https://developer.akamai.com/introduction/Prov_Creds.html) and [credentials](https://developer.akamai.com/introduction/Conf_Client.html) sections of the Get Started page on [the developer portal](https://developer.akamai.com).  
* When working through this process you need to give grants for the Identity Management V1 API.  The section in your configuration file should be called [idm]

```
[iam]
client_secret = [CLIENT_SECRET]
host = [HOST]
access_token = [ACCESS_TOKEN_HERE]
client_token = [CLIENT_TOKEN_HERE]
```

## Functionality

The following functionality are available:

* List the accountSwitchKeys and account names you can access based on the permissions of your API client
* Get an API client’s credentials
* Get details for a single credential
* View an API client’s details

## akamai-iam

This is the main program that wraps this functionality in a command line utility:

* [list-account-switch-keys](#list-account-switch-keys)
* [list-credentials](#list-credentials)
* [get-credential](#get-credential )
* [get-client](#get-client )

### list-account-switch-keys

Use this command to retrieve the accountSwitchKeys and account names you can access based on the permissions of your API client. Once you have the accountSwitchKeys you need, you can [make an API call to another account](https://learn.akamai.com/en-us/learn_akamai/getting_started_with_akamai_developers/developer_tools/accountSwitch.html#makeapicalls).

```bash
%  akamai iam list-account-switch-keys --open-identity-id pa444oyidwo6j4hy
```

The arguments available for this command are:

```
--open-identity-id <value>  A unique identifier for each API client.
--search <value>            Optionally filter results by accountId or accountName. Enter at least three characters in the string to filter the results.
--json                      Display output in json format (optional)
```

### list-credentials

Use this command to get an API client’s credentials

```bash
%  akamai iam list-credentials --open-identity-id pa444oyidwo6j4hy
```

The argument needed for this command is:

```
--open-identity-id <value>  A unique identifier for each API client.
--actions                   Optionally include actions option to get available actions that can be performed on the credentials
```

### get-credential

Get details for a single credential. Use Update a credential to change the credential’s expiration date, or toggle the credential’s activation status.

```bash
%  akamai iam get-credential --open-identity-id pa444oyidwo6j4hy --credential-id 345678
```

The arguments available for this command are:

```
--open-identity-id <value>  A unique identifier for each API client
--credential-id  <value>    A credential’s unique identifier.
--actions                   Optionally include actions option to get available actions that can be performed on the credential
```


### get-client

View an API client’s details. This operation lets you get a specific API client by passing the client’s token in the command.

```bash
%  akamai iam get-client --access-token akaa-onah2fsgph6i7sx2-j4vrsb3rbyqxuslo
```

The arguments available for this command are:

```
--access-token <value>  An access token identifies a collection of APIs belonging to an API client. Defaults to the access token of the current credential
--actions               Optionally include actions option to get available actions that can be performed on the client
```