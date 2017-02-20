# chatbotlib

Chatbotlib is a library that allows to define a chat (more to come...)

## Prerequisites 

* python 3+
* python pytohn-lxm


## Installing

Download the source code or clone the repository:

```
git clone htps://github.com/ 
```

## Running the examples

To run the examples just type 


```
path_to_chatlib>  python runbot.py -i botfile
```

Where *path_to_chatlib* is the root directory of the project and *botfile* is an bot definition xml.

## Tutorial and Examples

A chatbot is defined in an xml file containing a set of states. A state is defined in a **state** element. A state element must contain an attribute called **id**, an **start** element, and an **input** element. The **id** of the state will serve as an identifier to perform transitions between states. The **start** allows to specify the output when entering the state. The **input** element specify different cases to move to the next state according to the input. To do that, a set of cases should be specified using the **case** and **loopback** elements. 


The ouput of **start**, **case**, and **loopback** elements allows to specify different options to output text. The ouput is specified with a hierchical structure with the elements **sentence**, **random**, and **sequence**. A sentence specify a simple utterance to be displayed. A *delay* can be specified through the **delay** attribute. **random** and **sequence** elements are containers of **sentence** and containers, allowing to specify different effects. For example, the following start element will display a message:
```xml
<start>
  <sentence>Hello</sentence>
</start>  
```
The examples can be found in the **examples** folder. These are the detailed explanation of each one of the examples:

### Example 1: hello world

This example shows a deinition of a very simple chatbot. 

```xml
<chatbot-def start="greeting" bot-prompt="me: " user-prompt="you: ">

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

