# Anki-Edge-Extension
A Simple Anki Flash Card Creator Extension for Local Deployments

Creatd this Simple edge extension to make the fash card creations easy from the browser,Some example scenarios, but not limited to.
* `Want to create a flashcard for important facts found on the internet articles/blogs?`

### Disclaimer: 
* No Security features/functions used in these code. Please implement other controlls before using in the production.
* Some of the functions are not working as indended, but kept them for further implementations.

### Components: 
* Edge extension
* Backend python server to handle and create anki flashcards using the edge extention shared data.
* Anki local deployment
* AnkiConnect Add-on 



### Usage Instructions:
A) Instal Anki in the windows (can also be installed in linux) from https://apps.ankiweb.net/

And after installing, download the AnkiConnect Add-on (Tools/Add-Ons/Get-Addons) and use the code provided here https://ankiweb.net/shared/info/2055492159


B) Run the python backend server and make sure your machine can reach this backend server.

`python.exe py_server.py`

`E:\Anki-Edge-Extension> python.exe .\py_server.py`

![alt text](images\image-5.png)

C) 1) Launch Edge Browser and open extensions management page `edge://extensions/` and Enable `Developer mode`
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