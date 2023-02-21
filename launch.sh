#! /bin/sh

OUT=$1
TIME=180s

echo "" > ${OUT}
for file in ./instances/*
do
  echo ${file}
  echo ${file} >> ${OUT}
  timeout ${TIME} /usr/local/bin/python3.9 tower_sorting.py ${file} | grep -e "* " >> ${OUT}
  echo "\n\t\t************\n" >> ${OUT}
done
