#!/bin/bash
echo "Changing to AutoML Dir"
cd automl/
echo "Excuting Heroku Login"
heroku login
git init
git add .
echo "<<-- Starting Deployment -->>"
git commit -m "Pushed by AutoML CLI"
git push heroku master
echo "Deployment Completed!"