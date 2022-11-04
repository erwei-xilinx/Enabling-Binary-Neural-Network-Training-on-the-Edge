#!/bin/bash
output_dir='outputs'
mkdir -p $output_dir
result_file=${output_dir}'/results.txt'
touch $result_file
for l1 in '0.25' '0.5' '1'
do
for l2 in '0.25' '0.5' '1'
do
for l3 in '0.25' '0.5' '1'
do
for l4 in '0.25' '0.5' '1'
do
for l5 in '0.25' '0.5' '1'
do
for l6 in '0.25' '0.5' '1'
do
for l7 in '0.25' '0.5' '1'
do
for l8 in '0.25' '0.5' '1'
do
output_filename=${output_dir}'/'${l1}_${l2}_${l3}_${l4}_${l5}_${l6}_${l7}_${l8}'.txt'
echo $output_filename
python Binary.py ${l1} ${l2} ${l3} ${l4} ${l5} ${l6} ${l7} ${l8} > $output_filename
echo -n $l1 >> ${result_file}
echo -n " " >> ${result_file}
echo -n $l2 >> ${result_file}
echo -n " " >> ${result_file}
echo -n $l3 >> ${result_file}
echo -n " " >> ${result_file}
echo -n $l4 >> ${result_file}
echo -n " " >> ${result_file}
echo -n $l5 >> ${result_file}
echo -n " " >> ${result_file}
echo -n $l6 >> ${result_file}
echo -n " " >> ${result_file}
echo -n $l7 >> ${result_file}
echo -n " " >> ${result_file}
echo -n $l8 >> ${result_file}
cat $output_filename | tail -c -8 >> ${result_file}
done
done
done
done
done
done
done
done
