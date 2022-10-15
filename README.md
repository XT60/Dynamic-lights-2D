# 💡 Dynaimic Lights in 2D
This simple project represents my take on ray casting/tracing algorithm. 
First version I wrote was based on [this youtobe video](https://www.youtube.com/watch?v=fc3nnG2CG8U) 
that I strongly encourage you to watch if you are interseted in writing similar project. 
But unfortunatelly it wasn't fast enough to handle quite as much in python as it does in c++. 
I wasn't happy with the result so I read couple articles and got deeper into methodology. 
Eventually I gathered enough ideas to write my own version and this is the result

## 💻 Technologies used
- [![python 3.10.6](https://img.shields.io/badge/python-3.10.6-blue)](https://www.python.org/)
- [![pygame 2.1.2](https://img.shields.io/badge/pygame-2.1.2-green)](https://www.pygame.org/wiki/about)
- [![sortedcontainers 2.4.0](https://img.shields.io/badge/sortedcontainters-2.4.0-orange)](https://grantjenks.com/docs/sortedcontainers)

## 🏃 How to run
First of all to run this code you need to have Python3 on your machine, but thats not all. Easiest way to intall of dependencies is 
[use pip](https://pip.pypa.io/en/stable/installation/_=) and type in your terminal: 
```
pip install pygame --user
pip install sortedcontainters --user
```
If you prefer different way of installing or want to get more info on those dependencies links are above in technologies section.
Now, after installing all needed dependencies you are finally ready to run code locally on your mashine. But how do I do it if I never used python? I got you. Firstly open up terminale and navigate to folder where you installed all files from this repository 
``` 
cd /your/absoulte/file/path
```
Next step is to run the program with python, type in terminal:
```
python ./Loop.py
```
after confirming command new black window should popup with white rectangle in the 'middle'. This is window of the symulation now by clicking right mouse button you can add more obsticles to the environment and by clicking the right mouse button start raycasting simulation in realtime.


## 👩🏾‍💻 Author
<center>
 <img src="https://images.weserv.nl/?url=https://github.com/XT60.png?v=4&h=300&w=300&fit=cover&mask=circle&maxage=7d" alt="profileImg" width="30" height="30" align="left">
 <a href="[url](https://github.com/XT60)" align="left">XT60</a>
</center>


## ⏱️ Code performance
Python is not the first language when comes to mind when thinking about performance but the methodology presented in code is fast, at least fast enough to handle over 500 walls.


## 📚 More info
- https://www.youtube.com/watch?v=fc3nnG2CG8U
- https://ncase.me/sight-and-light/
- https://www.redblobgames.com/articles/visibility/

### 🚩 Problems
The downside to this sollution is that in current state it doesn't handle properly ray casting on contact point of two squares placed diagonally. 
This case is shown on image below.

<p align="center">
  <img src="https://user-images.githubusercontent.com/89086129/196006461-f1bf3621-44d8-4a37-87c0-2f2e78f4012d.png" alt="errorImg">
</p>
