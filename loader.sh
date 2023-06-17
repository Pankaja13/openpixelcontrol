i=1;

cmd_string=""

for file in "$@"
do
    cmd_string+=" -l $file"
    i=$((i + 1));
done

#echo "$cmd_string"
bin/gl_server $cmd_string

