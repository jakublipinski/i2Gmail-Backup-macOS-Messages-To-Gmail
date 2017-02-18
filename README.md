# Backup macOS Messages to Gmail

Have you ever lost your phone and all your important text messages? Have you ever struggled with finding a very important  message in your iMessage application? Is Gmail your main e-mail client? Check out i2Gmail!

i2Gmail is a Python utility which allows you to backup your iMessages from your macOS desktop computer to your Gmail account. If your macOS computer is [configured to send and receive SMS messages](https://support.apple.com/en-us/HT202549), your SMS messages will be backed up as well. Messages are stored on Gmail as regular emails. They are already read, archived, labeled as `Text` and easily searchable.

Please note: i2Gmail is in beta. Expect hick-ups. Please [report all the issues](https://github.com/jakublipinski/i2Gmail-Backup-macOS-Messages-To-Gmail/issues).

## Installation

In order to use i2Gmail you will need to:

### Clone the i2Gmail repository
```
git clone git@github.com:jakublipinski/i2Gmail-Backup-macOS-Messages-To-Gmail.git i2Gmail
cd i2Gmail
```
### Install google-api-python-client
```
easy_install --upgrade google-api-python-client
```
### Create your `client_secrets.json` file 
For i2Gmail to connect to your Gmail account you need to create a new application at Google APIs Console.

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

### Add your phone number and email to Gmail Contacts
Add your phone number and all your email addresses you use with iMessage to [Gmail Contacts](https://www.google.com/contacts/). 

### i2Gmail uses `Text` label
i2Gmail labals all the backed up messages with `Text`. If you already use such label, it's strongly recommened to change it to something else. You can change the label name in the `config.py` by modifing the `GMAIL_LABEL` variable.

## Backuping your Messages

### First backup

To start backup run:
```
python i2Gmail.py
```
A browser window will open asking to authorize the application against GMail. Choose the desired account and authorize the script. The backup procedure will start. The script will output its progress to the console. You can also follow the backup progress by searching for `label:text` in your Gmail account.

### Subsequent backup

To start subsequent backup run:
```
python i2Gmail.py
```
i2Gmail stores the last backed up message id in the file `settings.json` and backs up only new messages.

### Contacts Suggestions 

i2Gmail outputs duplicate email addresses and phone number which are assigned to different contacts. It's recommened to fix these duplicates so that i2Gmail assigns correct contact details to each message.

### Restarting backup

In order to start backup from scratch:
1. Remove the `settings.json` file
```
rm settings.json
```
2. Remove previously backed up messages from Gmail by searching `label:text`, selecting all messages and pressing `Delete` button

### Changing the Gmail account

In order to change the Gmail account to which the backup is performed delete the `credentials.storage` file. You will be asked to choose and authorize your Gmail account next time you run the script.

### Search your backed up messages.

You can search your backed up messages by ussing `label:text` search query in Gmail. You can combine it with other queries such as: `label:text from:me`, `label:text to:John`, etc

## Security

### Credentials needed
Application needs following Gmail permissions:
`Know who you are on Google` - to use your first and last name to indicate sender of your messages
`View your email address`	- to use your email address to indicate sender of your messages
`Insert mail into your mailbox`	- to backup your messages
`Manage mailbox labels` - to create `Text` label
`View your contacts` - to translate phone numbers and email addresses to people names

### Keep your files secured

Keep your `clients_secrets.json` and `credentials.storage` files secured. They give access to your Gmail account.

## Under the hood

### Original bearer

If you need to learn what was the original bearer of the message (SMS or iMessage) you can click `Show original` options from the dropdown menu next to your message and loook for `X-Original-Bearer` header.
