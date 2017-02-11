# Backup macOS Messages to Gmail

i2Gmail is a Python utility which allows you to backup your iMessages from your macOS desktop computer to your Gmail account. If your macOS computer is [configured to send and receive SMS messages](https://support.apple.com/en-us/HT202549) they will also be backed up. Messages are stored on Gmail as regular emails. They are already read, archived, labeled as `Text` and easily searchable.

Please note: i2Gmail is in beta. Expect hick-ups. Please [report all the issues](https://github.com/jakublipinski/i2Gmail-Backup-macOS-Messages-To-Gmail/issues).

## Installation

In order to use i2Gmail you will need:

### Clone the i2Gmail repository:
```
git clone git@github.com:jakublipinski/i2Gmail-Backup-macOS-Messages-To-Gmail.git i2Gmail
cd i2Gmail
```
### Install google-api-python-client
```
easy_install --upgrade google-api-python-client
```
### Create your Google Console project 

1. Go to [Google APIs Console](https://console.developers.google.com/flows/enableapi?apiid=gmail,contacts&credential=client_key)
  1. Verify that `Create a project` is selected
  2. Click the `Continue` button
  3. Within a few seconds, your project will be created. Click the `Go to Credentials`
  and the screen will display a confirmation message. On the confirmation screen, verify that all of the required APIs listed below are included. (Other APIs may also be enabled. You may ignore them.)


Required APIs:
Admin SDK
Apps Activity API



Create a new project

Add "OAuth client ID"
Choose Other

client_secrets.json

--noauth_local_webserver

add your email to contacts

https://stackoverflow.com/questions/27870024/google-gmail-api-installed-app-shows-ioerror-13-from-module-ssl-py-w-o-sudo
sudo chmod o+r /Library/Python/2.7/site-packages/httplib2-0.9.1-py2.7.egg/httplib2/cacerts.txt

contacts - emails instead of phone numbers (show original)



original Bearer
