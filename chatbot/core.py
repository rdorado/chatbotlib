import time, random, re, sys
from lxml import etree

class Chatbot:


   def __init__(self, initialStateID=None, botPrompt="", userPrompt="", context={}):
      self.initialStateID=initialStateID
      self.currentState=None
      self.botPrompt=botPrompt
      self.userPrompt=userPrompt
      self.finished = False
      self.waitingForInput = False 
      self.states = {}
      self.messageQueue = []
      self.functions = []
      self.isValid = None
      self.externChatbots = []
      self.context = context
      globals()['context'] = self.context


   def getBotPrompt(self):
      return self.botPrompt


   def getUserPrompt(self):
      return self.userPrompt

   def isWaitingForInput(self):
      return self.waitingForInput 


   def addFunction(self, function):
      self.functions.append(function)
   
   def addFunctionsFromCode(self, code):
      ind1 = code.find("def")
      while ind1 != -1: 
         indn = code.find("(",ind1+3)
         name = code[ind1+3:indn].strip() 
         ind2 = code.find("def", ind1+3)
         if ind2 == -1: 
            self.addFunction(Function(code,name=name))
         else: 
            self.addFunction(Function(code,name=name))
         ind1=ind2

   def addExternChatbot(self, externChatbot):
      self.externChatbots.append(externChatbot)
      if externChatbot.getName() not in self.states:
        self.states[externChatbot.getName()] = externChatbot


   def isFinished(self):
      return self.finished


   def getStateFromId(self, stateId):
      return self.states[stateId] 


   def setReady(self):
      self.currentState = self.getStateFromId(self.initialStateID)
      self.processState(self.currentState)


   def processState(self, state):
      startTP = state.getStart()
      messages = startTP.processAsList()
      self.messageQueue.extend(messages)
      self.waitingForInput = False


   def addState(self, state):
      self.states[state.getId()] = state


   def getNextMessage(self):
      if len(self.messageQueue) > 0:
         message = self.messageQueue.pop(0)
         delay = message.delay

         if delay > 0: time.sleep(delay)                  
         if len(self.messageQueue) == 0: self.waitingForInput = True

         return self.processMessage(message.text)

      self.waitingForInput = True
      return None 
      
   def processMessage(self, text):
      
      if "${" in text:
         indx1 = text.find("${")
         resp = text[:indx1] 
         while indx1 != -1: 
            indx2 = text.find("}", indx1+2)
            varname = text[indx1+2:indx2].strip()
            resp += context[varname]
            indx1 = text.find("${", indx2)
            if indx1!=-1: resp+=text[indx2+1:indx1]
            else: resp+=text[indx2+1:]
         return resp
      else:
        return text

   def processInput(self, string):
      state = self.currentState
      
      for case in state.getCases():
         nextStateId = case.match(string, self)
         if nextStateId != None:
            messages = []	
            case.getOutput().processAsList(messages)
            self.messageQueue.extend(messages)

            if nextStateId == None: 
               self.finished = True
               self.waitingForInput = False
            else:
               nextState = self.getStateFromId(nextStateId) 

               if isinstance(nextState, State):
                  self.currentState = nextState
               
                  messages = []
                  self.currentState.getStart().processAsList(messages)
                  self.messageQueue.extend(messages)
                  if self.currentState.isTerminalState(): self.finished = True 
                  else: self.finished = False
                      
                  self.waitingForInput = False 

               elif isinstance(nextState, ExternChatbot):  
                  self.load(nextState.getSrc())
 
            return

      if state.hasLoopback():
         messages = [] 
         state.getLoopback().getOutput().processAsList(messages)
         self.messageQueue.extend(messages)
         self.finished = False
         self.waitingForInput = False          


   def clear(self):
      pass

   
   ############################################################################################################
   #
   #  XML loading methods
   ############################################################################################################
   def load(self, filename):

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

       self.clear()
       self.__init__(start, botPrompt, userPrompt, context=self.context)

       for el in root.getchildren():
         if el.tag == "state":
            self.readState(el)	
         elif el.tag == "function":
            self.readFunction(el)
         elif el.tag == "code":
            self.readCode(el)
         elif el.tag == "extern-chatbot":
            self.readExternalChatbot(el)

       self.executeOnStart()
       self.setReady()
       return self
    
     except FileNotFoundError as err:
       print("File not found: '"+filename+"'")
       sys.exit(2)

   def executeOnStart(self):
      for funct in self.functions:
         if funct.getName() == "onStart": 
            exec(funct.getSource())
            exec("onStart()")
            return

   def readExternalChatbot(self, root):
      self.addExternChatbot(ExternChatbot(root.attrib['name'], root.attrib['src']))

   def readCode(self, root):
     try:
       exec(root.text)
     except SyntaxError as e:
       print("Error loading the following code:\n\n"+root.text)
       print(e)
       sys.exit(2)
     self.addFunctionsFromCode(root.text)


   def readFunction(self, root):
     try:
       exec(root.text)
     except SyntaxError as e:
       print("Error loading the following function:\n\n"+root.text)
       print(e)
       sys.exit(2)
     self.addFunction(Function(root.text))


   def readState(self, root):
      state = State(root.attrib["id"])
   
      for el in root.getchildren():

         if el.tag == "start":
            state.setStart( self.readStart(el) )           
         elif el.tag == "input":
            state.setInputProcessor( self.readInput(el) )           
      self.addState(state)


   def readStart(self, root):
      resp = TextContainer()
      for el in root.getchildren():
         if el.tag == "sentence":
           resp.addElement( self.readSentence(el) )           
         elif el.tag in ["random","sequence"]:
           self.readContainer(el, resp)          
      return resp


   def readInput(self,root):
      resp = InputProcessor()
      for el in root.getchildren():
         if el.tag == "case": 
            resp.addCase( self.readCase(el) )
         elif el.tag == "loopback":
            resp.setLoopback( self.readLoopback(el)) 
      return resp


   def readLoopback(self, root):
      resp = Case()

      outp = TextContainer()
      self.readContainer(root, outp)
      resp.setOutput(outp)

      return resp


   def readCase(self, root):
      resp = Case()

      outp = TextContainer()
      self.readContainer(root, outp)
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


   def readSentence(self,root):
      delay = 0

      try:
        delay = float(root.attrib["delay"])
      except KeyError: pass

      sent = Sentence(root.text, delay)
      return sent


   def readContainer(self, root, container=None):
      if root.tag == "random":
         cont = TextContainer("random")
      else: 
         cont = TextContainer("sequence")

      if container!=None:
         container.addElement(cont)

      for el in root.getchildren():
         if el.tag == "sentence":
           cont.addElement( self.readSentence(el) )           
         elif el.tag in ["random","sequence"]:
           self.readContainer(el, cont)     
        
      return cont




#################################################################
# Class Message
#################################################################
class Message:

   def __init__(self, text, delay=0):
      self.text=text
      self.delay=delay



#################################################################
# Class ExternChatbot
#################################################################
class ExternChatbot:

   def __init__(self, name, src):
      self.name=name
      self.src=src

   def getName(self):
      return self.name

   def getSrc(self):
      return self.src


   def setName(self, name):
      self.name=name

   def setSrc(self, src):
      self.src=src

#################################################################
# Class State
#################################################################
class Function:
   
   def __init__(self, src, name=None):
      if name==None:
         self.name = self.getFunctionNameFromSource(src)
      else: 
         self.name = name 
      self.src = src
 
   def getFunctionNameFromSource(self, src):
      resp = ""
      ind1 = src.find("def")
      ind2 = src.find("(", ind1+3)
      return src[ind1+3:ind2].strip()

   def getName(self):
      return self.name

   def getSource(self):
      return self.src

#################################################################
# Class State
#################################################################
class State:

   def __init__(self, id):
      self.id=id
      self.inputProcessor=None

   def setInputProcessor(self, inputElement):
      self.inputProcessor=inputElement

   def setStart(self, start):
      self.start = start

   def getStart(self):
      return self.start

   def getId(self):
      return self.id

   def getCases(self):
      if self.inputProcessor == None: return []
      return self.inputProcessor.cases

   def hasLoopback(self):
      return self.getLoopback() != None

   def getLoopback(self):
      if self.inputProcessor == None: return None
      return self.inputProcessor.getLoopback()

   def isTerminalState(self):
      return len(self.getCases())==0 and not self.hasLoopback()


#################################################################
# Class Sentence
#################################################################
class Sentence:

   def __init__(self, text, delay=0):
      self.text=text
      self.delay=delay

   
#################################################################
# Class Code
#################################################################   
class Code:

   def __init__(self, code):
      self.code=code


#################################################################
# Class InputProcessor
#################################################################   
class InputProcessor:
   
   def __init__(self):
      self.cases = []
      self.loopback = None


   def addCase(self, case):
      self.cases.append(case)

   def setLoopback(self, case):
      self.loopback = case

   def getLoopback(self):
      return self.loopback


#################################################################
# Class Case
#################################################################   
class Case:

   def __init__(self):
      self.pattern = None
      self.type = None      
      self.function = None
      self.output = None
      self.nextStateId = None

   def setOutput(self, output):
      self.output = output

   def getOutput(self):
      return self.output

   def setType(self, typeStr):
      self.type = typeStr

   def setPattern(self, pattern):
      self.pattern = pattern
      self.compiled = re.compile(pattern)
   
   def setFunction(self, function):
      self.function = function

   def match(self, string, bot):
      if self.type == "pattern":
         if self.compiled.match(string) != None:
            return self.nextStateId
         else: return None
      elif self.type == "function":
         for funct in bot.functions:
            if funct.getName() == self.function: 
              exec(funct.getSource())
              exec("global resp\nresp = "+self.function+"(string)")
         return resp

   def setNextStateId(self, string):
      self.nextStateId = string 
         
   def getNextStateId(self):
      return self.nextStateId
   

#################################################################
# Class TextContainer
################################################################# 
class TextContainer:

   def __init__(self, type=None):
      self.container = []
      if type == "random":
         self.type="random"
      else:
         self.type="sequence"

   def addElement(self,element):
      self.container.append(element) 
   
   def processAsList(self, resp=[]):

      if self.type == "random":
    
         sel = random.randint(0, len(self.container)) - 1
         self.processElement(self.container[sel], resp)
        
      else:

         for elem in self.container:
            self.processElement(elem, resp)
      
      return resp

   def processElement(self, elem, resp):
      if isinstance(elem, TextContainer):
         elem.processAsList(resp)
      elif isinstance(elem, Sentence):
         resp.append( Message(elem.text, elem.delay) )
      elif isinstance(elem, Code):
         pass
  

#################################################################
# Class Output
################################################################# 
class Output:
   
   def __init__(self, type):
      pass

   def addElement(self, element):
      pass




