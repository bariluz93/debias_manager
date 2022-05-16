#!/bin/bash
set -e


SHORT=c,p,t,m:,h
LONG=collect_embedding_table,preprocess,translate,model:,help
OPTS=$(getopt -a -n debias --options $SHORT --longoptions $LONG -- "$@")

eval set -- "$OPTS"

collect_embedding_table=""
preprocess=""
translate=""
model=""
while :
do
  case "$1" in
    -c | --collect_embedding_table )
      collect_embedding_table="-c"
      shift 1
      ;;
    -p | --preprocess )
      preprocess="-p"
      shift 1
      ;;
    -t | --translate )
      translate="-t"
      shift 1
      ;;
    -m | --model )
      model="$2"
      shift 2
      ;;
    -h | --help)
      echo "usage:
Mandatory arguments:
  -m, --model                     the translation model .
Optional arguments:
  -c, --collect_embedding_table   collect embedding table .
  -p, --preprocess                preprocess the anti dataset .
  -t, --translate                 translate the entire dataset .
  -h, --help                      help message ."
      exit 2
      ;;
    --)
      shift;
      break
      ;;
    *)
      echo "Unexpected option: $1"
      exit 1;;
  esac
done



if [ "${model}" == "" ]; then
  echo missing argument model
  exit 1
fi

case $model in
    0|1) echo ;;
    *) echo "argument model can get only the values 0 for Nematus or 1 to easyNMT"
       exit 1;;
esac

if [ "$model" == '1' ]; then
  if [[ "$collect_embedding_table" == "-c" || "$preprocess" == "-p" ]]; then
    echo cannot pass --collect_embedding_table and --preprocess with easyNMT
    exit 1
  fi
fi