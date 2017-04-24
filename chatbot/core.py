import time
import random
import re

class Chatbot:

   def __init__(self, initialStateID, botPrompt, userPrompt):
      self.initialStateID=initialStateID
      self.currentState=None
      self.botPrompt=botPrompt
      self.userPrompt=userPrompt
      self.finished = False
      self.waitingForInput = False 
      self.states = {}
      self.messageQueue = []
      self.functions = []

   def isWaitingForInput(self):
      return self.waitingForInput 

   def addFunction(self, string):
      self.functions.append(string)

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

         return message.text

      self.waitingForInput = True
      return None 
      
   def processInput(self, string):
      state = self.currentState
      
      for case in state.getCases():
         if case.match(string, self):
            messages = []	
            case.getOutput().processAsList(messages)
            self.messageQueue.extend(messages)
            
            nextStateId = case.getNextStateId()

            if nextStateId == None: 
               self.finished = True
               self.waitingForInput = False
            else:
               self.currentState = self.getStateFromId(nextStateId)
               messages = []
               self.currentState.getStart().processAsList(messages)
               self.messageQueue.extend(messages)
               if self.currentState.isTerminalState(): self.finished = True 
               else: self.finished = False
                      
               self.waitingForInput = False    
            return

      if state.hasLoopback():
         messages = [] 
         state.getLoopback().getOutput().processAsList(messages)
         self.messageQueue.extend(messages)
         self.finished = False
         self.waitingForInput = False          


class Message:

   def __init__(self, text, delay=0):
      self.text=text
      self.delay=delay


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

class Sentence:

   def __init__(self, text, delay=0):
      self.text=text
      self.delay=delay

   
      
class Code:

   def __init__(self, code):
      self.code=code



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
         return self.compiled.match(string) != None
      elif self.type == "function":
         for funct in bot.functions:
            exec(funct) 
         exec("global resp\nresp = "+self.function+"(string)")
         return resp

   def setNextStateId(self, string):
      self.nextStateId = string 
         
   def getNextStateId(self):
      return self.nextStateId
   

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
  


class Output:
   
   def __init__(self, type):
      pass

   def addElement(self, element):
      pass




