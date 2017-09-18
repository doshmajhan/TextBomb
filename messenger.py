"""
    Messin around

	7/18/2017
	@author: Doshmajhan
"""

import os
import json
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


SERVICE_MAPPINGS = {
    "at&t": "mms.att.net",
    "sprint": "messaging.sprintpcs.com",
    "verizon": "vzwpix.com",
    "t-mobile": "tmomail.net"
}


class Messenger(object):
    """
        Class to provide the messenger api
    """

    def __init__(self, email, password):
        self.contacts = load_contacts()
        self.server = None
        self.email = email
        self.password = password

    def send(self, message):
        """
            Function to send a message to our list of contacts

            :param message: the message string to be sent
        """
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.starttls()
        self.server.login(self.email, self.password)

        for contact in self.contacts:
            domain = SERVICE_MAPPINGS[contact['carrier']]
            address = "{}@{}".format(contact['number'], domain)
            print "From: {} - To: {}".format(self.email, address)
            self.server.sendmail(self.email, address, message)

        self.server.quit()

def load_contacts():
    """
        Function to load our contacts from the contacts.json file

        :returns contacts: an array of the contacts in the json file
    """
    with open('contacts.json') as data:
        contacts_json = json.load(data)

    return contacts_json["contacts"]


def main():
    """
        Main function to initiate our messengers and send our message
    """
    img_data = open('patrick.jpg', 'rb').read()
    message = MIMEMultipart()
    image = MIMEImage(img_data, name=os.path.basename('patrick.jpg'))
    message.attach(image)

    with open('creds.txt') as accounts:
        account_list = [acc.split(",") for acc in accounts.readlines()]
        messengers = [Messenger(email, password) for email, password in account_list]

    for messenger in messengers:
        for _ in range(4):
            messenger.send(message.as_string())


if __name__ == "__main__":
    main()
