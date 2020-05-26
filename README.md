# marathondraw

Running the project:
---
You will need python 3+ version installed.
Also recommended to use viritual env to install the modules to run
the project.
You can do so by doing this:
```
> python -m venv venv # creates a venv folder, use python3 instead of python if u have python2 installed as well
> venv\Scripts\activate # to activate the venv, 
> deactivate # use this when u want to stop using venv
```

To install libraries, u can use the requirements list or specify them
yourself
```
> pip install -r requirements.txt
```

Now you can run the servers on different tabs:
```
> python serve_front.py # this will start the frontend pages as live server on multiple ports
> python serve_back.py # starts the game server
```
