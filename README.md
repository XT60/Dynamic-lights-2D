# 💡 Dynaimic Lights in 2D
This simple project represents my take on ray casting/tracing algorithm. 
First version I wrote was based on [this youtobe video](https://www.youtube.com/watch?v=fc3nnG2CG8U) 
that I strongly encourage you to watch if you are interseted in writing similar project. 
But unfortunatelly it wasn't fast enough to handle quite as much in python as it does in c++. 
I wasn't happy with the result so I read couple articles and got deeper into methodology. 
Eventually I gathered enough ideas to write my own version and this is the result
Running the code opens window where you can place walls to you liking and test how algorithm in action.

## Technologies used
- python for logic
- pygame  library for graphisc redering

## 📖 Author
- [XT60](https://github.com/XT60)

## ⏱️ Code performance
Python is not the first language when comes to mind when thinking about performance but the methodology presented in code is fast, at least fast enough to handle over 500 walls.

## More info
 - https://www.redblobgames.com/articles/visibility/
 - https://ncase.me/sight-and-light/
 - https://www.youtube.com/watch?v=fc3nnG2CG8U

### 🚩 Problems
The downside to this sollution is that in current state it doesn't handle properly ray casting on contact point of two squares placed diagonally. 
This case is shown on image below.

<p align="center">
  <img src="https://user-images.githubusercontent.com/89086129/195985620-b59d068e-5902-42df-81fc-b16c9fc98066.png" alt="errorImg">
</p>
