# Hackathon2020
![OurLogo](https://github.com/asl11/Hackathon2020/blob/master/logo.png?raw=true)
MeetSafe is a Web Application designed to facilitate safe and responsible returns back to in person meetings. 

Organizations and Institutions can use our tool to get an optimized meeting room assignment. Our tool works by 
taking in data regarding where people start at, as well as which meetings they need to go to at certain times. 
Then, by developing a graph to model the paths within the building or campus, our model will assign meetings 
to rooms such that the amount of contact when travelling to meetings is minimized. Our model also can filter
by room name, or interaction score, so that companies can decide which meetings might be best to move online.

The Code:
Our backend is built in Flask at api/api.py. It calls functions in optimize.py/run_optimization.py that handles 
the model optimization. Our frontend is built in React, the main file being fronten/src/app.js. To use our site, 
run api.py and app.js through two terminal windows, visit localhost:3000, and optimize your meetings!



