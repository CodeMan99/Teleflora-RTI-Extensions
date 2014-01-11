#!/usr/bin/env python3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright by Cody A. Taylor on 2013-December-22

import os.path
import sys
from smtplib import SMTP, SMTPRecipientsRefused
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
#import cx_Oracle as oracle

"""SendEmails.py - Automates sending order photos to the customer

To send a photo to a customer simply call this program with order
number and the path to the photo(s) you want to send.

See README.txt for more detailed directions and information.
"""

__all__ = ["main", "_read_file", "_read_data", "_query_database"]
__author__ = "Cody A. Taylor"
__version__ = "1.0.broken"

def main(*args):
    #dictionary<string,list<string>>; key=ordernumber: value=list of image_file_path
    input = {args[i - 1]: args[i].split(",") for i in range(1, len(args), 2)}
    data = {}
    data.update(_read_data("Settings.txt"))
    
    header = _read_data("Email-Header.txt")
    alternate_body_string = _read_file("Email-Format.txt")
    body_string = _read_file("Email-Format.html")
    
    with db.connect(data["dbuser"], data["dbpasswd"], data["dbserver"]) as connection:
        cursor = connection.cursor()

        with SMTP("smtp.gmail.com", 587) as gmail:
            gmail.ehlo()
            gmail.starttls()
            gmail.ehlo()
            gmail.login(data["gmail_user"], data["gmail_passwd"])

            for ordernumber in input:
                data["ordernumber"] = ordernumber
                data.update(_query_database(cursor, ordernumber))

                message = MIMEMupltipart("mixed")

                for key in header:
                    message[key] = header[key].format(**data)

                body = MIMEMultipart("alternative")
                body.attach(MIMEText(alternate_body_string.format(**data)))
                body.attach(MIMEText(body_string.format(**data)))
                message.attach(body)

                for image_path in input[ordernumber]:
                    with open(image_path, "rb") as image:
                        message.attach(MIMEImage(image.read(), name=os.path.basename(image_path)))

                try:
                    gmail.sendmail(data["gmail_user"], data["client_email"], message.as_string())
                except SMTPRecipientsRefused:
                    print("Failure: Email did not send to {client_email} for ordernumber {ordernumber}".format(**data), file=sys.stderr)
                else:
                    print("Success: Email sent to {client_email} for ordernumber {ordernumber}".format(**data))

    return 0

def _read_file(filename):
    s = ""

    with open(filename) as e:
        s = e.read()

    return s

def _read_data(filename):
    d = {}

    with open(filename) as s:
        d.update(line.strip().split(": ") for line in s)

    return d

def _query_database(cursor, ordernumber):
    rows = None

    if "oracle" in dir():
        cursor.execute("SELECT name, email, recipient FROM orders WHERE ordernum=:on;", on=ordernumber)
        rows = cursor.fetchall()
    else:
        ## Test data when the database is not available
        rows = [("Cody", "codemister99@yahoo.com", "Jackie Soo")]

    assert len(rows) == 1, """\
Expected exactly one (1) row from the database query.
  Received '{}' rows.""".format(len(rows))

    return {k: v for k, v in zip(("client", "client_email", "recipient"), rows[0])}

if __name__ == "__main__":
#    sys.exit(main(*sys.argv[1:]))