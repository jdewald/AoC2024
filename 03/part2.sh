 grep -E -o "do\(\)|don't\(\)|mul\([0-9]{1,3},[0-9]{1,3}\)" |\
	 awk 'BEGIN { yes = 1} /do\(/ { yes=1 } /don/ { yes=0 } /mul/ && yes == 1 { print }' |\
       	 sed -E 's#mul\(([^,]+),([^,]+)\)#\1 * \2#g' | bc | awk '{tot+=$1} END { print tot }'
