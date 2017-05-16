#!/usr/bin/env python

########################################################################################################################
#
#
#
#
########################################################################################################################

import urllib2
import subprocess
import shutil
import re
import os
from time import sleep

########################################################################################################################
# Create variables and prompt user for input.
########################################################################################################################

webPage = ""
phoneNumber = ""
emailAddress = ""

print "URL from Class you are looking to register for?"
webPage = raw_input().strip()
print "Apple Phone Number or ID?(hit enter for none)"
phoneNumber = raw_input()
print "Email Address(hit enter for none)"
emailAddress = raw_input()
print "Wright State UID"
uid = raw_input()
print "Wright State Pin"
pin = raw_input()

crnNumber = webPage[-5:];

########################################################################################################################
#
#
#
#
#
########################################################################################################################
while True:
    try:
        #Create default variables
        webText = urllib2.urlopen(webPage).read()
        tableBeginIndex = 0;
        tableEndIndex = 0;
        numberOfSeatsRemaining = 0;

        #Find out if the webpage uses has a cross-list section or not.
        if webText.find("<SPAN class=\"fieldlabeltext\">Cross List Seats</SPAN>") != -1:
            tableBeginIndex = webText.find("<SPAN class=\"fieldlabeltext\">Cross List Seats</SPAN>")
        else:
            tableBeginIndex = webText.find("<SPAN class=\"fieldlabeltext\">Seats</SPAN>")

        #Cut off the front of the webpage
        webText = webText[tableBeginIndex:]
        #Cut off the end of the webpage
        tableEndIndex = webText.find("</tr>")
        webText = webText[:tableEndIndex]

        #Clycle through the Table data, splicing the webText further each time
        for x in range(0, 3):
            goldenNumber = re.search(r'[0-9]+', webText)
            tableBeginIndex = webText.find(goldenNumber.group())
            if tableBeginIndex != -1:
                webText = webText[tableBeginIndex+ len(goldenNumber.group()):]
            numberOfSeatsRemaining = goldenNumber.group()

        #Test print the seats remaining
        #print int(numberOfSeatsRemaining)

        #Alert users depending on preference
        if int(numberOfSeatsRemaining) > 0:
            if phoneNumber != "":
                os.system("osascript text.scpt " + phoneNumber)
            if emailAddress != "":
                os.system("./automateEmail.py" + emailAddress)

            ############################################################################################################
            #
            ############################################################################################################
            # Read all content from the original template for the Login html
            content = ""
            with open('./userLogin/_login.htm', 'r') as content_file:
                content = content_file.read()

            # Insert the default value of the your UID you added
            insertChange = content.find("type=\"text\" name=\"sid\" size=\"11\" maxlength=\"9\" id=\"UserID\"")
            content = content[:insertChange] + " value = \"" + uid + "\" " + content[insertChange:]

            # Insert the default value of the your UID you added
            insertChange = content.find("type=\"password\" name=\"PIN\" size=\"15\" maxlength=\"14\"")
            content = content[:insertChange] + " value = \"" + pin + "\" " + content[insertChange:]

            # Write to the new file; thus preserving the template
            with open("./userLogin/_newLogin.htm", "w") as text_file:
                text_file.write(content)

            subprocess.call(['open', "./userLogin/_newLogin.htm"])
            sleep(10)

            ############################################################################################################
            # Because of Cookie issues, the browser mush have your username and password previously saved. Needs
            # further testing to optimize.
            ############################################################################################################
            #Read all content from the original template for the website's html
            content = ""
            with open('./automaticAdd/_original.htm', 'r') as content_file:
                content = content_file.read()

            #Insert the default value of the class you want added
            insertChange = content.find("id=\"crn_id1\"")
            content = content[:insertChange] + "value = \"" + crnNumber + "\" " + content[insertChange:]

            #Write to the new file; thus preserving the template
            with open("./automaticAdd/_newAdd.htm", "w") as text_file:
                text_file.write(content)

            #Use the default OS app to open the html file
            subprocess.call(['open', "./automaticAdd/_newAdd.htm"])

    #Catch all exceptions
    except:
        print "Something went horribly wrong"
    sleep(300)
