# cli-idm
Provides a way to interact with Identity Management related information via Open APIs. Functionality includes ...

## Local Install
* Python 3+
* pip install -r requirements.txt

### Credentials
In order to use this module, you need to:
* Set up your credential files as described in the [authorization](https://developer.akamai.com/introduction/Prov_Creds.html) and [credentials](https://developer.akamai.com/introduction/Conf_Client.html) sections of the Get Started pagegetting started guide on developer.akamai.comthe developer portal.  
* When working through this process you need to give grants for the Identity Management V1 API.  The section in your configuration file should be called [idm]
```
[idm]
client_secret = [CLIENT_SECRET]
host = [HOST]
access_token = [ACCESS_TOKEN_HERE]
client_token = [CLIENT_TOKEN_HERE]
```