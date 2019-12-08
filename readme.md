
## About Kachuva

Kachuva (turtle in Nepali) is ros package similar to turtlesim build with python . This is DIY project intended for the ROS learner for creating ros application .

## Installation

1. Install Dependencies
```
sudo apt-get install python-pygame
```

2. Compile Main Package
```
cd ~/catkin_ws/src/
git clone https://github.com/santoshdahal2016/Kachuva-ros-turtlesim-python.git kachuva
cd ~/catkin_ws && catkin_make
```


## Teleop Kachuva

This process needs to execute operation after any key is pressed . Obviously, in a case like that I don't want line buffering -- I want the program to execute operation as soon as I press a key, not wait until I hit Enter and then read the whole line at once. In Unix that's called "cbreak mode".

There are a few ways to do this in Python. The most straightforward way is to use the curses library, which is designed for console based user interfaces and games such as pygames. But importing curses is overkill just to do key reading.