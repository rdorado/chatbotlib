# chatbotlib

Chatbotlib is a library that allows to define a chat (more to come...)

## Prerequisites 

* python 3+
* python pytohn-lxm


## Installing

Download the source code or clone the repository:

```
git clone https://github.com/rdorado/chatbotlib
```

## Running the examples

To run the examples just type 
```
path_to_chatlib>  python runbot.py -i botfile
```
Where *path_to_chatlib* is the root directory of the project and *botfile* is an xml file with the bot's logic.

## Tutorial and Examples

A chatbot is defined in an xml file containing a set of states. A state is defined in a **state** element. A state element must contain an attribute called **id**, an **start** element, and an **input** element. The **id** of the state will serve as an identifier to perform transitions between states. The **start** allows to specify the output when entering the state. The **input** element specify different cases to move to the next state according to the input. To do that, a set of cases should be specified using the **case** and **loopback** elements. 


The ouput of **start**, **case**, and **loopback** elements allows to specify different options to output text. The ouput is specified with a hierchical structure with the elements **sentence**, **random**, and **sequence**. A sentence specify a simple utterance to be displayed. A *delay* can be specified through the **delay** attribute. **random** and **sequence** elements are containers of **sentence** and containers, allowing to specify different effects. For example, the following **start** element will display a "Hello" message:
```xml
<start>
  <sentence>Hello</sentence>
</start>  
```
The following start element will select randomly between the sentences "Hi!" and "Hello!":
```xml
<start>
  <random>
    <sentence>Hi!</sentence>
    <sentence>Hello!</sentence>
  </random>   
</start>  
```
The examples can be found in the **examples** folder. These are the detailed explanation of each one of the examples:

### Example 1: hello world

This example shows a definition of a very simple chatbot. It starts with a sentence, wait for the user's input, and finally says good bye and terminates.
```xml
<chatbot-def start="greeting">

  <state id="greeting">

    <start>
      <sentence>hello world! say something!</sentence>
    </start>   
   
    <input>
      <case type="pattern" pattern=".*">
        <sentence delay="1.3">Ok! good bye!</sentence>
      </case>
    </input>

  </state>

</chatbot-def>
```
To run this example execute:
```
path_to_chatlib>  python runbot.py -i hello_world.bot
```
### Example 2: greeting

This example shows the selection of two different sequences randomly.
```xml
<chatbot-def start="greeting">

  <state id="greeting">

    <start>
      <random>
        <sentence>hi!</sentence>
        <sentence delay="1.5">hello!</sentence>
      </random>
      <random>
        <sentence>how are you?</sentence>
        <sentence delay="1.5">are you there?</sentence>     
      </random>
    </start>   
   
    <input>
      <case type="pattern" pattern=".*">
        <sentence delay="1.3">Ok! good bye!</sentence>
      </case>
    </input>

  </state>

</chatbot-def>
```
To run this example execute:
```
path_to_chatlib>  python runbot.py -i greeting.bot
```
### Example 3: greeting 2
This example shows the usage of the **loopback** element to return to the same state. The bot will finish only if the user says "hi".
```xml
<chatbot-def start="greeting">

  <state id="greeting">

	   <start>
       <random>
	       <sentence>hi!</sentence>
	       <sentence>hello!</sentence>
       </random>
	   </start>  

	   <input>
       <case type="pattern" pattern=".*hi.*">
         <sentence>Have a nice day!</sentence> 
       </case>
       <loopback>
         <random>
           <sentence>Just say, hi</sentence>
           <sentence>It is rude not say hi</sentence>
           <sentence>You only need to say hi</sentence>
         </random>
       </loopback>
     </input>

  </state>

</chatbot-def>
```
To run this example execute:
```
path_to_chatlib>  python runbot.py -i greeting2.bot
```
### Example 4: greeting 3
This example shows a complex randomization of a greeting.
```xml
<chatbot-def start="greeting" bot-prompt="me: " user-prompt="you: ">

  <state id="greeting">

    <start>
      <random>
        <sentence delay="0.4">hi!</sentence>
        <sentence delay="0.4">hello!</sentence>
      </random>
      <sentence delay="1.9">How are you?</sentence>
      <random>
        <sequence>
          <sentence delay="2.1">Are you ok?</sentence>
          <sentence delay="2.1">hello?</sentence>
        </sequence>
        <sequence>
          <sentence delay="2.1">Is this a good time?</sentence>
          <sentence delay="2.1">Seems your are busy....</sentence>
        </sequence>
      </random>  
    </start>   
   
    <input>
      <case type="pattern" pattern="(.*)">
        <sentence delay="1.4">Good bye!</sentence>
      </case>
    </input>
  </state>

</chatbot-def>
```
To run this example execute:
```
path_to_chatlib>  python runbot.py -i greeting3.bot
```
### Example 5: survey
This example shows an application of a survey app, where the objectives are:
* Ask two questions to the user
* Give the user the option to 'quit' the test
* Force the user to answer only 'yes' or 'no'
The example shows also how to use and to make transitions between states.
```xml
<chatbot-def start="greeting" bot-prompt="me: " user-prompt="you: ">

  <state id="greeting">

    <start>
      <sequence>
        <sentence>Welcome!</sentence>
        <sentence delay="2.5">Thank you, very much for taking our survey!</sentence>
        <sentence delay="2.5">You will have to answer two yes/no questions. Please type only 'yes' or 'no'.</sentence>
        <sentence delay="2.5">If you want to quit type 'quit', otherwise please tell us your name.</sentence>
      </sequence>
    </start>   
   
    <input>
      <case type="pattern" pattern="quit">
        <sentence delay="1.3">Ok! good bye!</sentence>
      </case>
      <case type="pattern" pattern="quit" next="end"/> 
      <case type="pattern" pattern=".*" next="q1"/>              
    </input>

  </state>


  <state id="q1">

    <start>
      <sentence delay="1.3">First question: do you smoke?</sentence>  
    </start>

    <input>
      <case type="pattern" pattern="yes" next="q2"/>
      <case type="pattern" pattern="no" next="q3"/>
      <loopback>
        <sentence delay="1.3">Please type only yes or no.</sentence>
      </loopback>  
    </input>   

  </state>


  <state id="q2">

    <start>
      <sentence delay="1.3">Do you want to quit?</sentence>  
    </start>

    <input>
      <case type="pattern" pattern="yes" next="end"/>
      <case type="pattern" pattern="no" next="end"/>
      <loopback>
        <sentence delay="1.3">Please type only yes or no.</sentence>
      </loopback>  
    </input>   

  </state>


  <state id="q3">

    <start>
      <sentence delay="1.3">Have you smoked in the last year?</sentence>  
    </start>

    <input>
      <case type="pattern" pattern="yes" next="end"/>
      <case type="pattern" pattern="no" next="end"/>
      <loopback>
        <sentence delay="1.3">Please type only yes or no.</sentence>
      </loopback>  
    </input>   

  </state>


  <state id="end">

    <start>
      <sentence delay="1.3">Thank you very much!</sentence>  
    </start>

  </state>

</chatbot-def>
```
To run this example execute:
```
path_to_chatlib>  python runbot.py -i survey.bot
```

## Future developments

* Include the execution of other 'chatbots' inside the definition of a chatbot.
* Add entity extraction functionalities.
* Add a probabilistic model, where the random element allows a multinomial distribution with different probabilites for each sentences. It will allow also to 'learn' from the different executions.
