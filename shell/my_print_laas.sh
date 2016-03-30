

if [ -z "$1" ]
  then
    echo " --You should input an argument : the file name (and not the path)"
    echo " -- Go to the folder wanted and send the file name"
fi


# File to print
FILE=$1

# copy the file to verdier and send instruction to print from there
scp $FILE mmoreaux@verdier:~/
ssh mmoreaux@verdier "lp -d calvino $FILE"
