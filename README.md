# chatbotlib

Chatbotlib is a library that allows to define a chat (more to come...)

## Prerequisites 

* python 3+
* python pytohn-lxm


## Installing

Download the source code or clone the repository:

```git clone htps://github.com/ 
```

## Running the examples

To run the examples just type 


```path_to_chatlib>  python runbot.py -i botfile
```

Where *path_to_chatlib* is the root directory of the project and *botfile* is an bot definition xml.

## Tutorial and Examples

The examples can be found in the **examples** folder. These are the detailed explanation of each one of the examples:

### Example 1: hello world

This example shows a deinition of a very simple chatbot. 

```<chatbot-def start="greeting" bot-prompt="me: " user-prompt="you: ">

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

