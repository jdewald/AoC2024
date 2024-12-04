 grep -E -o 'mul\([0-9]{1,3},[0-9]{1,3}\)' | sed -E 's#mul\(([^,]+),([^,]+)\)#\1 * \2#g' | bc | awk '{tot+=$1} END { print tot }'
