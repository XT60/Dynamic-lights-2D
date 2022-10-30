# 💡 Dynamic Lights in 2D
This simple project represents my take on the ray casting/tracing algorithm. 
The first version I wrote was based on [this youtobe video](https://www.youtube.com/watch?v=fc3nnG2CG8U) 
that I strongly encourage you to watch if you are interested in writing a similar project. 
Unfortunatelly, it wasn't fast enough to handle quite as much in python as it does in c++. 
I wasn't happy with the performance, so I read couple of articles and got deeper into the methodology. 
Eventually, I gathered enough ideas to write my own version and this is the result.

## 💻 Technologies used
- [![python 3.10.6](https://img.shields.io/badge/python-3.10.6-blue)](https://www.python.org/)
- [![pygame 2.1.2](https://img.shields.io/badge/pygame-2.1.2-green)](https://www.pygame.org/wiki/about)
- [![sortedcontainers 2.4.0](https://img.shields.io/badge/sortedcontainters-2.4.0-orange)](https://grantjenks.com/docs/sortedcontainers)

## 🏃 How to run
First of all, to run this code you need to have Python3 on your machine, but it doesn't end here. You also need to install all dependencies. 
The easiest way to do it is to [use pip](https://pip.pypa.io/en/stable/installation/_=) and type in your terminal: 
```
pip install pygame --user
pip install sortedcontainters --user
```
If you prefer a different way of installing or want to get more information on those dependencies, the links are above in the technologies section.
Now, after installing all the needed dependencies, you are finally ready to run code locally on your machine. But how do I do it? 
Again you will need to open up a terminal window and navigate to the folder where you installed all the files from this repository.
In this case ***cd*** is command you will need.
``` 
cd /your/absoulte/file/path
```
Next step is to run the program with python, type in terminal:
```
python ./Loop.py
```
If everything is set up correctly after confirming the command with *enter* black window with white rectangle should pop up. 
This is the simulation window and this means you are ready to start playing.
Actions you can take are:
 - add more obsticles to the environment by clicking the right mouse button 
 - start raycasting simulation in realtime by clicking the right mouse button


## 👨‍💻 Author
<center>
 <img src="https://images.weserv.nl/?url=https://github.com/XT60.png?v=4&h=300&w=300&fit=cover&mask=circle&maxage=7d" alt="profileImg" width="30" height="30" align="left">
 <a href="[url](https://github.com/XT60)" align="left">XT60</a>
</center>


## ⏱️ Code performance
Python is not the first language that comes to mind when thinking about performance but the methodology presented in code is quite fast. I am still working on optimising it even further. Right now it can easily handle around 200 walls. After exceeding that number it gets laggy but is still usable up to 700 ish, depending on the structure of shapes.


## 📚 More info
- https://www.youtube.com/watch?v=fc3nnG2CG8U
- https://ncase.me/sight-and-light/
- https://www.redblobgames.com/articles/visibility/


## 🛠️ How is it different from classic solution?
Well, firstly, what I was trying to accomplish was to cast as little rays and create a polygon with as little vertices as possible. So at the begining of the main polygon-exctracting function I sort all the points by an angle relative to the current mouse position. In the v1 version I changed it a little by not directly calculating angles with the trigonometric functions and instead using the matrix determinant to determine the points's order. After sorting I calculate how many walls intersect with the light ray at the relative 0 angle, so that while iterating through points I can keep walls that currently can be intersected by light ray and not applying the line intersection algorithm to every wall. Also while iterating I keep a top_wall value that represents wall that was the closeest in latest itertion, this way I can reduce amout of points to minimum by placing exactly 2 (start and end of section) points on every wall that appears in the solution except the first wall in the sollution. 
So inn short:
- sorting points by angle (retrieved by matrix determinant)
- iterating through sorted points and for each casting a ray
- not checking walls that will surely not intersect with the light ray
- minimising amount of vertices that polygon contains of -> exacly 2 points for every wall which part is included (except begining wall)
For more insight I recomment checking my code yourself :)


### 🚩 Problems
The downside to this solution is that in the current state it doesn't properly handle ray casting on contact the point of two squares placed diagonally. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/89086129/196006461-f1bf3621-44d8-4a37-87c0-2f2e78f4012d.png" alt="errorImg">
</p>
