find . -size  0 -print0 |xargs -0 rm
nof=$(($(ls | wc -l) - $(ls *py| wc -l) - $(ls *csv| wc -l) - $(ls *pl| wc -l)-$(ls *sh| wc -l)-$(ls *temp| wc -l) ))
echo $nof
