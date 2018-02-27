from lxml import etree
import sys
from chatbot.core import Chatbot

class ReadChatbotDefinitionException(Exception):

   def __init__(self, message):
      self.message = message


def load(filename,context={}):
  c = Chatbot(context=context)
  c.load(filename)
  return c

'''
  try: 
    parser = etree.XMLParser()
    tree = etree.parse(filename, parser)
    root = tree.getroot()
    # TODO: validate with an Schema or a DTD

    start=root.attrib["start"]
    if "bot-prompt" in root.attrib:
      botPrompt=root.attrib["bot-prompt"]
    else:
      botPrompt="chatbot> "
    if "user-prompt" in root.attrib:
      userPrompt=root.attrib["user-prompt"]
    else:
      userPrompt="you> "

    bot = chatbot.core.Chatbot(start, botPrompt, userPrompt)
    
    for el in root.getchildren():
      if el.tag == "state":
         readState(bot, el)	
      elif el.tag == "function":
         readFunction(bot,el)

    bot.setReady()
    return bot
    
  except FileNotFoundError as err:
    print("File not found: '"+filename+"'")
    sys.exit(2)
'''

  
