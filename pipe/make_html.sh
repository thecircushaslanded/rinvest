for i in *.txt; do
    sed '1,/html/d' $i > $i.html
done
