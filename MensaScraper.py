# -*- coding: utf-8 -*-
"""
Created on Thu Jan  26 20:15:30 2019

@author: Thomas
"""

# Load packages 
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import pandas as pd

# Define necessary functions

# Function that fetches today's menu as list from the webAddress you give
def menuToday(webAddress):
    html = urlopen(webAddress)
    bsObj = BeautifulSoup(html.read(), "html5lib")
    tag = bsObj.find("a", {"name":"heute"})
    menu = tag.find_parent().find_next_sibling()
    menuList = []
    for p in menu.findAll("p"):
        newItem = p.get_text()
        menuList.append(newItem)
    return(menuList)

# Function that compares 2 menus and returns list which indicated differences
def menuCompare(mensaA, mensaB):
    mensaA = set(mensaA)
    mensaB = set(mensaB) 
    menu = list(mensaA & mensaB)
    mensaAOnly = [item for item in mensaA if item not in mensaB]
    mensaAOnly = [s + " (Mensa only)" for s in mensaAOnly]
    mensaBOnly = [item for item in mensaB if item not in mensaA]
    mensaBOnly = [s + " (stuBistro only)" for s in mensaBOnly]
    menu = ("\n".join(menu + mensaAOnly + mensaBOnly))
    return(menu)

# Day stuff
dayOfWeek = datetime.today().weekday()
now = datetime.now()
today = now.strftime("%d.%m.%Y")

#
html = urlopen("https://www.studentenwerk-muenchen.de/mensa/speiseplan/speiseplan_412_-de.html#heute")
bsObj = BeautifulSoup(html.read(), "html5lib")
tag = bsObj.find("a", {"name":"heute"})
heute = tag.find_parent().find('strong').get_text()

#today = heute

# doing the work
if dayOfWeek > 4:
    pass
elif heute != today:
    emailText = str("Hi there," + "\n" + "Bad news: The mensa is closed today!")
else :
    # Get menus of both mensas
    mensaMenu = menuToday("https://www.studentenwerk-muenchen.de/mensa/speiseplan/speiseplan_412_-de.html#heute")
    stuBistroMenu = menuToday("https://www.studentenwerk-muenchen.de/mensa/speiseplan/speiseplan_415_-de.html#heute")
    # Start writing the email
    emailText = str("Hi there," + "\n" + "This is the menu for the Mensas in Martinsried:" + "\n\n")
    emailText = emailText + \
                menuCompare(mensaMenu, stuBistroMenu) + \
                "\n\n" + "Enjoy your meal!" + "\n" + "\n" + "P.S." + "\n" + "The labels mean the following:" + "\n"
    # Add what the labels mean
    labels = str()
    labelBlock = bsObj.find("ul", {"class":"c-schedule__type-list"})
    for li in labelBlock:
        newLabel = re.sub("\t+","",li.get_text().replace("\n","").strip())
        newLabel = newLabel.replace(")",")\t\t")
        newLabel = newLabel.replace("(Bio-Bayern)\t","(Bio-Bayern)")
        labels = labels + newLabel + "\n"
    emailText = emailText + labels

#print(emailText)

# Set up the email
df = pd.read_csv('mensaScraperEmailList.csv')
recipients = df.email_address.tolist()
    
fromaddr = "Mensa.Alerts089@gmail.com"
toaddr = ["thomas.vanemden@bmc.med.lmu.de"]
toBcc = recipients
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['Subject'] = "Today's Mensa Menu"
body = emailText
msg.attach(MIMEText(body, 'plain'))

# Send the email
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("Mensa.Alerts089@gmail.com", "CurryWurst")
text = msg.as_string()
server.sendmail(fromaddr, [toaddr] + toBcc , text)
server.quit()