# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 20:15:30 2019

@author: Thomas
"""

# Load packages 
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

dayOfWeek = datetime.today().weekday()

now = datetime.now()
today = now.strftime("%d.%m.%Y")

html = urlopen("https://www.studentenwerk-muenchen.de/mensa/speiseplan/speiseplan_412_-de.html#heute")
bsObj = BeautifulSoup(html.read(), "html5lib")
tag = bsObj.find("a", {"name":"heute"})
heute = tag.find_parent().find('strong').get_text()

if dayOfWeek >5:
    pass
elif heute != today:
    emailText = str("Hi there," + "\n" + "Bad news: The mensa is closed today!")
else :
    html = urlopen("https://www.studentenwerk-muenchen.de/mensa/speiseplan/speiseplan_412_-de.html#heute")
    bsObj = BeautifulSoup(html.read(), "html5lib")
    tag = bsObj.find("a", {"name":"heute"})
    menu = tag.find_parent().find_next_sibling()
    emailText = str("Hi there," + "\n" + "Today's Mensa Menu is:" + "\n" + "\n")
    for p in menu.findAll("p"):
        emailText = emailText + p.get_text() + "\n"
    emailText = emailText + "\n" + "Enjoy your meal!"

fromaddr = "Mensa.Alerts089@gmail.com"
toaddr = ['lucia.caballero@bmc.med.lmu.de', "matias.capella@bmc.med.lmu.de", "thomas.vanemden@bmc.med.lmu.de"]
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ', '.join(toaddr)
msg['Subject'] = "Today's Mensa Menu"
 
body = emailText
msg.attach(MIMEText(body, 'plain'))
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("Mensa.Alerts089@gmail.com", "CurryWurst")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()