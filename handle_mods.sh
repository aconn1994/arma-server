cd steamcmd/arma3/steamapps/workshop/content
find . -depth -exec rename 's/(.*)\/([^\/]*)/$1\/\L$2/' {} \;