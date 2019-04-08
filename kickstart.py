import json
import os
import subprocess
import xml.etree.ElementTree as ET
from functions import *


currentDirectory = os.path.dirname(os.path.realpath(__file__))

with open(currentDirectory + '/kickstart-config.json', 'r') as bootstrapConfigFile:
    bootstrapConfigJSON = json.load(bootstrapConfigFile)

##XML Candidate Config Manipulation
#note: right now we are just manipulating password for admin, end goal is to create an api-admin
paloConfigXML = ET.parse(currentDirectory + '/candidateConfig.xml').getroot()
#update admin password
# if paloConfigXML[0][0][0].attrib['name'] == 'admin':
#     paloConfigXML[0][0][0][0].text = boostrapConfigJSON['bootstrap']['palo']['palo-admin-password-hash']
for xmlData in paloConfigXML[0][0]:
    if xmlData.tag == 'phash':
        xmlData.text = boostrapConfigJSON['bootstrap']['palo']['palo-admin-password-hash']
    if xmlData.tag == 'public-key':
        xmlData.text = boostrapConfigJSON['bootstrap']['palo']['palo-admin-public-key']
