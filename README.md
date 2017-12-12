# SeeFood @ Illinois
This repo contains the backend for SeeFood @ Illinois, an app that recognizes dining hall food from pictures.

## Hosting
This API is hosted on Heroku at the url https://seefood-illinois.herokuapp.com

## Running the server locally
All requirements are listed in requirements.txt, use pip to install them.
```
gunicorn __init__:app --timeout 120
```
The server will be run on localhost:8000, and will have all the functionality of the online server.

## How to use
To run the comparison code, make a POST request to https://seefood-illinois.herokuapp.com/recognize/(hall)/(meal).
The POST request should contain a JSON with a field "description". This description should contain a string with space separated words which contain the Clarifai output from describing the image (see https://www.clarifai.com/models/food-image-recognition-model/bd367be194cf45149e75f01d59f77ba7). A JSON will be returned with a field "matches" which contains an array with the names of the top five matches of the food recognition code from that particular meal.

Written by Thomas Huang
