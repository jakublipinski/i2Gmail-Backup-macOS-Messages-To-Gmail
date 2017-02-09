easy_install --upgrade google-api-python-client


Go to:
https://console.developers.google.com/flows/enableapi?apiid=gmail&credential=client_key

Create a new project

Add "OAuth client ID"
Choose Other

client_secrets.json

--noauth_local_webserver

https://stackoverflow.com/questions/27870024/google-gmail-api-installed-app-shows-ioerror-13-from-module-ssl-py-w-o-sudo
sudo chmod o+r /Library/Python/2.7/site-packages/httplib2-0.9.1-py2.7.egg/httplib2/cacerts.txt