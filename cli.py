#!/bin/env/python

# -*- coding: utf8 -*-

import sys
import os

from ConfigParser import ConfigParser
from optparse import OptionParser, Option, OptionGroup

from lib import SoneraSMS

__AUTHOR__ = u"Pekka Järvinen"
__YEAR__ = "2013"
__VERSION__ = "0.0.1"


if __name__ == "__main__":
  banner = u" Sonera SMS Sender %s" % (__VERSION__)
  banner += u" (c) %s %s" % (__AUTHOR__, __YEAR__)

  examples = []
  examples.append('--recipient 0401234567 --message "Hello from Python!"')
  examples.append('--createconfig')
  examples.append('--createconfig --configfile /home/raspi/.smscfg')
  examples.append('--configfile /home/raspi/.smscfg --recipient 0401234567 --message "Hello from Python!"')

  usage = "\n".join(examples)

  parser = OptionParser(version="%prog " + __VERSION__, usage=usage, description=banner)

  parser.add_option("--recipient", "-r", action="store", type="string", dest="recipient", help="Recipient's phone number")
  parser.add_option("--message", "-m", action="store", type="string", dest="message", help="Message")
  parser.add_option("--createconfig", "-n", action="store_true", dest="createcfgfile", help="Create config file", default=False)
 
  parser.add_option("--configfile", "-c", action="store", type="string", dest="cfgfile", help="Use different config file", default=os.path.join(os.path.expanduser("~"), ".sonerasms"))
  parser.add_option("--debug", "-v", action="store", type="string", dest="debug", help="Prints more information")

  (options, args) = parser.parse_args()

  if len(sys.argv) == 1:
    print("See --help for usage information")
    sys.exit(1)

  if options.createcfgfile:
    print("Creating file '%s' ..") % options.cfgfile
    cfg = ConfigParser()
    cfg.add_section("auth")
    cfg.set("auth", "username", "myuser")
    cfg.set("auth", "password", "mypass")
    with open(options.cfgfile, 'w') as f:
      cfg.write(f)
    print("Done. Now add your credentials to that file.")
    sys.exit()

  if not os.path.isfile(options.cfgfile):
    print("Config file '%s' not found. Create one with --create.") % options.cfgfile
    sys.exit(1)

  if options.recipient and options.message:
    cfg = ConfigParser()
    cfg.read(options.cfgfile)

    sms = SoneraSMS.SoneraSMS(cfg.get("auth", "username"), cfg.get("auth", "password"))

    if not sms.login():
      print("Error: Unable to login. Check your credentials.")
      sys.exit(1)

    if sms.send(options.recipient, options.message):
      print("Message sent successfully")
      sys.exit()

    print("Error: Message was not sent! Check recipient and message.")
    sys.exit(1)

  else:
    print("See --help for usage information")
    sys.exit(1)

  sys.exit(1)
