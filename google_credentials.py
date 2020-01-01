from __future__ import print_function
import config

import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client import file

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class GoogleCredentials:

    # Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
    OAUTH_SCOPE = ['https://www.googleapis.com/auth/userinfo.email',
                   'https://www.googleapis.com/auth/gmail.insert',
                   'https://www.googleapis.com/auth/gmail.labels',
                   'https://www.googleapis.com/auth/contacts.readonly']

    def authenticate(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        store = oauth2client.file.Storage(config.CREDENTIALS_STORAGE_FILE)
        self.credentials = store.get()
        if not self.credentials or self.credentials.invalid:
            flow = client.flow_from_clientsecrets(config.CLIENT_SECRET_FILE,
                                                  self.OAUTH_SCOPE)
            flow.user_agent = config.APPLICATION_NAME
            if flags:
                self.credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                self.credentials = tools.run(flow, store)
            print('Storing credentials to ' + config.CREDENTIALS_STORAGE_FILE)

        self.email = self.credentials.id_token['email']
