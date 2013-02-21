#!/bin/env/python
# -*- coding: utf8 -*-
#
# Send SMS messages through Sonera's web page
# Uses Requests - http://python-requests.org/
#
# (c) Pekka Järvinen 2013

import os
import sys
import re

import requests

class SoneraSMS:
  # Username (usually phone number)
  _user = None

  # Password
  _pass = None

  # Requests session (remembers cookies etc)
  _ses = None

  def __init__(self, user, password):
    self._user = user
    self._pass = password

  def login(self):
    if self._user is None or self._user == "":
      raise Exception("User is not defined")

    if self._pass is None or self._pass == "":
      raise Exception("Password is not defined")

    # Start new session 
    self._ses = requests.Session()

    # Get cookie crap
    self._ses.get("https://www4.sonera.fi/login/Login")

    # Login

    payload = {
      "authmethod": "basic",
      "user": self._user,
      "password": self._pass,
      "submit": "submit",
      "login_page": "/login/Login",
    }

    r = self._ses.post("https://www4.sonera.fi/login/Login", data=payload)

    if 'set-cookie' in r.headers:
      if 'profile' in r.headers["set-cookie"]:
        return True

    return False

  def send(self, recipient, message):
    if self._ses is None:
      raise Exception("Requests session is not started!")

    # Get more cookie crap
    r = self._ses.get("https://www4.sonera.fi/OmatSivut/?Matkapuhelin_Viestit_Tekstiviesti")

    payload = {
      "action": "",
      "mode": "sms",
      "recip": recipient,
      "message": message,
      "$folderstore": "0",
      "regularMessage": "",
      "js_smsused_val": "1",
      "composer": "send",
      "gindex": "1"
    }

    # Send SMS message
    r = self._ses.post("https://www4.sonera.fi/vk/www/index.jsp", data=payload)

    # Confirm sending
    match = re.match(r".*Viesti.*L.*hetetty.*\d+.*vastaanottajalle.*onnistuneesti.*", r.text, re.MULTILINE|re.IGNORECASE|re.DOTALL) 

    if match:
      return True   
    return False

# Example:	
if __name__ == "__main__":
  sms = SoneraSMS("myuser", "mypass")
  if sms.login():
    if sms.send("0401234567", "Hello from Python!"):
      print("Sent successfully!")
    else:
      print("Something went wrong while sending :(")
