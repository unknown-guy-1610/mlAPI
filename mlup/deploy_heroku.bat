@echo off

ECHO Changing to AutoML Dir
PUSHD automl

CALL heroku
IF ERRORLEVEL 1 GOTO NOTFOUND

git remote show heroku | find "heroku" > NUL & IF ERRORLEVEL 1 (
    ECHO App not found!!
    CALL heroku create
    ECHO App created and remote origin is set!!) ELSE (
    ECHO App exists!!
)


ECHO Adding all files to heroku!!
git init
git add . && git commit  
git push heroku master -f
IF ERRORLEVEL 1 (
    ECHO Some Error Occured!!
    EXIT /B
)
ECHO Site deployed!!
EXIT /B

:NOTFOUND
ECHO Heroku CLI not present!!
EXIT /B