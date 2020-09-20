# Hackathon2020
![Page1](https://github.com/asl11/Hackathon2020/blob/master/websitePreview/1.png?raw=true)
![Page2](https://github.com/asl11/Hackathon2020/blob/master/websitePreview/2.png?raw=true)
![Page3](https://github.com/asl11/Hackathon2020/blob/master/websitePreview/3.png?raw=true)
![Page4](https://github.com/asl11/Hackathon2020/blob/master/websitePreview/4.png?raw=true)


MeetSafe is a Web Application designed to facilitate safe and responsible returns back to in person meetings. 

Organizations and Institutions can use our tool to get an optimized meeting room assignment. Our tool works by 
taking in data regarding where people start at, as well as which meetings they need to go to at certain times. 
Then, by developing a graph to model the paths within the building or campus, our model will assign meetings 
to rooms such that the amount of contact when travelling to meetings is minimized. Our model also can filter
by room name, or interaction score, so that companies can decide which meetings might be best to move online.

## The Code:

Our backend is built in Flask at api/api.py. It calls functions in optimize.py/run_optimization.py that handles 
the model optimization. Our frontend is built in React, the main file being fronten/src/app.js. To use our site, 
run api.py and app.js through two terminal windows, visit localhost:3000, and optimize your meetings! You'll need
to install node.js / its packages, as well as some python packages.

## Data Inputs:

PersonTable contains information about each person in the organization.

    PersonID - Numeric Identifier of Person
    Name - Name of Person
    MeetingID - Meeting that each person is assigned to
    PersonalRoomID - Room that person starts in

MeetingTable contains information about each meeting.

    MeetingID - Numeric Identifier of each Meeting
    MeetingName - Name of Meeting
    MeetingTime - Start time of a meeting

LocationTable contains information about each location in the organization.

    LocationID - Numeric Identifier of each meeting
    LocationName - Name of location
    Capacity - COVID safe capacity of each location

NetworkTable contains all locations that have an edge between them. We use this to create an undirected graph.

    Node 1 - The source node
    Node 2 - The target node
    Edge_Weight - The weight of the edge between Node 1 and Node 2

