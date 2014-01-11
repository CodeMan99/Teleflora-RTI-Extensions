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
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
#import cx_Oracle as oracle

"""SendEmail.py - Automates sending order photos to the customer

To send a photo to a customer simply call this program with order
number and the path to the photo(s) you want to send.

See README.txt for more detailed directions and information.
"""

__all__ = ["main", "_read_file", "_read_data", "_query_database"]
__author__ = "Cody A. Taylor"
__version__ = "0.2"

def main(*args):
    data = {"ordernumber": args[0]}
    data.update(_read_data("Settings.txt"))
    data.update(_query_database(data["rti_user"], data["rti_passwd"], args[0]))

    message = MIMEMultipart("mixed")

    email_header = _read_data("Email-Header.txt")
    for key in email_header:
        message[key] = email_header[key].format(**data)

    body = MIMEMultipart("alternative")

    body.attach(
        MIMEText(
            _read_file("Email-Format.txt").format(**data),
            "plain"
        )
    )
    body.attach(
        MIMEText(
            _read_file("Email-Format.html").format(**data),
            "html"
        )
    )

    message.attach(body)

    for path in args[1].split(","):
        with open(path, "rb") as image:
            message.attach(
                MIMEImage(
                    image.read(),
                    name=os.path.basename(path)
                )
            )

    with SMTP("smtp.gmail.com", 587) as gmail:
        gmail.ehlo()
        gmail.starttls()
        gmail.ehlo()
        gmail.login(data["gmail_user"], data["gmail_passwd"])
        gmail.sendmail(
            data["gmail_user"],
            data["client_email"],
            message.as_string()
        )

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

def _query_database(username, password, ordernumber):
    rows = None

    if "oracle" in dir():
        ## The following code is untested
        with oracle.connect(username, password, "localhost:1521/XE") as connection:
            cursor = connection.cursor()
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
    sys.exit(main(*sys.argv[1:]))