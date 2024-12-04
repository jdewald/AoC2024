 join <(sort -n input.txt | awk '{print NR,$1}') <(sort -k2 -n input.txt | awk '{print NR,$2}') |  awk '{ diff=$2-$3; if (diff < 0) { diff=-diff }; tot+=diff; print diff } END { print tot }'
