#! /bin/sh

for filepath
do
    filename=$(basename $filepath)
    docid=${filename%.txt}
    outfile=${filepath/%txt/xml}
    echo "<doc id=\"$docid\">" > $outfile
    cat $filepath >> $outfile
    echo "</doc>" >> $outfile
done
