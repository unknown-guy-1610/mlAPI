echo "Changing to working Dir"
cd $1

var1="$(which heroku)"

if echo $var1 | grep -q "heroku"; then
    echo "Herku cli present!!"
else
    echo "Heroku cli not present!!"
    exit 1
fi

var2="$(git remote show heroku)"

if echo $var2 | grep -q "heroku"; then
    echo "App Exists !!"
else
    echo "App not found!!"
    command heroku create
    echo "App created and remote origin is set!" 
fi

echo "Adding all files to heroku!!"

var3="$(git rev-parse --is-inside-work-tree 2>/dev/null)"
if [ "$var3" ]; then
  echo "Repo already Initialized"
else
  git init
fi


{
    git add . && git commit  
    git push heroku master -f 
    echo "Site deployed!!"
    exit 1
} || {
    echo "Some Error Occured!!"
    exit 1
}
    
