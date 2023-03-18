echo $'{' > hash_table.json
i=0
while read p; do
  echo "    \"$p\": "$i, >> hash_table.json
  ((i=i+1))
done < common_paths.txt
 printf '%s\n' '$' 's/.$//' wq | ex hash_table.json
echo "}" >> hash_table.json