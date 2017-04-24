from lxml import etree
import sys
import chatbot.core

class ReadChatbotDefinitionException(Exception):

   def __init__(self, message):
      self.message = message

def load(filename):

  try: 
    parser = etree.XMLParser()
    tree = etree.parse(filename, parser)
    root = tree.getroot()
    # TODO: validate with an Schema or a DTD

    start=root.attrib["start"]
    botPrompt=root.attrib["bot-prompt"] 
    userPrompt=root.attrib["user-prompt"]

    bot = chatbot.core.Chatbot(start, botPrompt, userPrompt)
    
    for el in root.getchildren():
      if el.tag == "state":
         readState(bot, el)	
      elif el.tag == "function":
         readFunction(bot,el)

    bot.setReady()
    return bot
    
  except FileNotFoundError as err:
    print("No such file or directory: '"+filename+"'")
    sys.exit(2)

def readFunction(bot, root):
  bot.addFunction(root.text)

  try:
    exec(root.text)
  except SyntaxError as e:
    print("Error loading the function '"+root.attrib['name']+"'")
    print(e)
    sys.exit(2)

def readState(bot, root):
   state = chatbot.core.State(root.attrib["id"])
   
   for el in root.getchildren():

      if el.tag == "start":
         state.setStart( readStart(el) )           
      elif el.tag == "input":
         state.setInputProcessor( readInput(el) )           
   bot.addState(state)

def readStart(root):
   resp = chatbot.core.TextContainer()
   for el in root.getchildren():
      if el.tag == "sentence":
        resp.addElement( readSentence(el) )           
      elif el.tag in ["random","sequence"]:
        readContainer(el, resp)          
   return resp


def readInput(root):
   resp = chatbot.core.InputProcessor()
   for el in root.getchildren():
      if el.tag == "case": 
         resp.addCase( readCase(el) )
      elif el.tag == "loopback":
         resp.setLoopback( readLoopback(el)) 
   return resp

def readLoopback(root):
   resp = chatbot.core.Case()

   outp = chatbot.core.TextContainer()
   readContainer(root, outp)
   resp.setOutput(outp)

   return resp

def readCase(root):
   resp = chatbot.core.Case()

   outp = chatbot.core.TextContainer()
   readContainer(root, outp)
   resp.setOutput(outp)
   
   try:
      ctype = root.attrib["type"]
   except KeyError:
      print("Type attribute is mandatory for case elements, line "+str(root.sourceline))
      sys.exit(2)

   resp.setType(ctype)

   if ctype == "pattern": 

      try: 
         resp.setPattern(root.attrib["pattern"])
      except KeyError: 
         print("A pattern should be specified for a case of type pattern, line "+str(root.sourceline))
         sys.exit(2)

   elif ctype == "function":

      try: 
         resp.setFunction(root.attrib["name"])
      except KeyError: 
         print("The name of a function should be specified for a pattern of type function, line "+str(root.sourceline))
         sys.exit(2)

   try:
      nextState = root.attrib["next"] 
      resp.setNextStateId(nextState)
   except:
      pass

   return resp

def readSentence(root):
   delay = 0

   try:
     delay = float(root.attrib["delay"])
   except KeyError: pass

   sent = chatbot.core.Sentence(root.text, delay)
   return sent


def readContainer(root, container=None):
   if root.tag == "random":
      cont = chatbot.core.TextContainer("random")
   else: 
      cont = chatbot.core.TextContainer("sequence")

   if container!=None:
      container.addElement(cont)

   for el in root.getchildren():
      if el.tag == "sentence":
        cont.addElement( readSentence(el) )           
      elif el.tag in ["random","sequence"]:
        readContainer(el, cont)     
        
   return cont

  
