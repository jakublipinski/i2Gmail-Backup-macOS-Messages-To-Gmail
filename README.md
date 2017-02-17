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
### Create your `client_secrets.json` file 

1. Go to [Google APIs Console](https://console.developers.google.com/flows/enableapi?apiid=gmail,contacts&credential=client_key)
2. Verify that `Create a project` is selected
3. Click the `Continue` button
4. Within a few seconds, your project will be created. Click the `Go to Credentials`.
5. Click the `Credentials` from the menu on the left side.
6. Go to the `OAuth consent screen` tab.
7. Enter `i2Gmail` into the `Product name shown to users` box. Press `Save`.
8. Go to the `Credentials` tab if not taken there automatically.
9. Click the 'Create credentials` blue button dropdown and select `OAuth client ID`.
10. Select `Other` from the list, enter `Console client` into `Name` field and press `Create`.
11. Close the pop-up window.
12. Click the `Download JSON` arrow located on the right side of the `Console client` label.
13. Save the file into the `i2Gmail` folder as `client_secrets.json`


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
