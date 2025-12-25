# Anki-Edge-Extension
Creatd this Simple edge extension to make the fash card creations easy from the browser, Some example scenarios, but not limited to.
* `Want to create a flashcard for important facts found on the internet articles/blogs?`


### Disclaimer: 
* No Security features used in these code. Please implement other security controlls before using in the production.
* Some of the functions are not working as indended, but kept them for further implementations.

### Components: 
* Edge extension
* Backend python server to handle and create anki flashcards using the edge extention shared data.
* Anki local deployment
* AnkiConnect Add-on

### How Does It Work?:
Using the Browser extension, 
1) The user can select the text(which becomes the answer) they want to create the Flashcard.
2) User should provider the question to the flashcard and optional Tags in the pop-up window.
3) After submiting the data, the details are sent to the local python server (it can also be a remote host), where the data received from the user machine is processed and deck and flashcards are created.

Note: If there is any error's raised during the Flashcards creation, then these errors only recorded in the python server, No feedback is given to the enduser. 


### Usage Instructions:
A) Instal Anki in the windows (can also be installed in linux) from https://apps.ankiweb.net/

And after installing, download the AnkiConnect Add-on (Tools/Add-Ons/Get-Addons) and use the code provided here https://ankiweb.net/shared/info/2055492159


B) Run the python backend server and make sure your machine can reach this backend server.

`Change the global variables, if required in the python script`

`python.exe py_server.py`

`E:\Anki-Edge-Extension> python.exe .\py_server.py`

![alt text](images\image-5.png)

C) Install Anki Browser Extension
1) Launch Edge Browser and open extensions management page `edge://extensions/` and Enable `Developer mode`
![alt text](images\image.png) 

2) Use `Load unpacked` option to selec the folder where the extension is located ![alt text](images\image-1.png)

Once the extensions is installed, we can use the context menus to create new flashcards

3) Select any text you want to create a Q&A flashcard. The selected text will be copied into the answer inbox, but we can edit this if requried. 

![alt text](images\image-2.png)

    And right click and select "Create Anki Flash card" option to open the popup window

![alt text](images\image-4.png)

4) Edit the questions and Answers as per your need

5) Tags are used to indicate in which Decks we need to create this Flashcard. 

the backend python script will check if the deck is already created or we need to create new one. 

If we already have a flashcard with same question, it'll try to create a new question by appending `(1)` at the end of the question.

6) After submiting, the pop-up will be closed, (currently there is no feedback to user)

D) Inspect the Anki to check if cards are created or not?
![alt text](images\image-6.png)