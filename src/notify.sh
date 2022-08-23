if [ -z "$1" ] || [ -z "$1" -a "$1" == "remove" ]; then
	echo "Usage:"
	echo "sh notify.sh add [tag] [url] [token] [price]"
	echo "sh notify.sh remove <tag>"
	echo "sh notify.sh list"
elif [ "$1" == "add" ]; then
	if [ -z "$2" ]; then
		read -p "Enter tag: " tag
	else
		export tag="$2"
	fi
	if [ -z "$3" ]; then
		read -p "Enter url: " url
	else
		export url="$3"
	fi
	if [ -z "$4" ]; then
		read -p "Enter token: " token
	else
		export token="$4"
	fi
	if [ -z "$5" ]; then
		read -p "Enter price: " price
	else
		export price="$5"
	fi
	

	nohup python main.py --token $token --url $url --max $price >/dev/null 2>&1 & 
	export pid=$!
	
	echo "${tag}|${pid}|${price}|${url}" >> data.txt
elif [ "$1" == "remove" ]; then
	if [ ! -f "data.txt" ]; then
		echo "No tracked ads."
	fi
	export pid=`grep -m 1 "^$2\|" data.txt | awk '{split($0,a,"|"); print a[2]}'`
    echo $pid
    #kill $pid
	grep -vwE "^$2" data.txt > data2.txt
    mv data2.txt data.txt
elif [ "$1" == "list" ]; then
	if [ ! -f "data.txt" ]; then
		echo "No tracked ads."
	else 
        cat data.txt
    fi
fi

