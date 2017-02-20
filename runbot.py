import chatbot.loader
import sys, getopt
import traceback

def main(argv):

    #    
    #  Reads the arguments, in particular the name of the xml file where the bot definition is
    #  expected. 
    #
    inputfile = None    
    try:
      opts, args = getopt.getopt(argv,"hi:", ["ifile="])
    except getopt.GetoptError:
      usage()
      sys.exit(2)

    for opt, arg in opts:
      if opt == '-i':
        inputfile = arg
    
    if inputfile == None: 
      usage()
      sys.exit(2)

       

    #
    #  This is the main part. It shows how to use the current implementation to 
    #  work in a synchronous way. 
    #
    try:
       bot = chatbot.loader.load(inputfile)         
       
       while not bot.isFinished():

          while not bot.isWaitingForInput():
               message = bot.getNextMessage()
               print("bot: "+message)	
          
          userInput = input('user: ') 
          bot.processInput(userInput) 

       while not bot.isWaitingForInput():
               message = bot.getNextMessage()
               print("bot: "+message)	
          

    except:
        traceback.print_exc()

#
#  A function that prints the usage using a terminal
#
def usage():
    print('usage: chatbot.py -i <chatbotfile>')

if __name__ == "__main__":
    main(sys.argv[1:])


