#!/bin/bash
set -e


SHORT=c,p,t,d,b,e,m:,h
LONG=collect_embedding_table,preprocess,translate,debias_encoder,begining_decoder_debias,end_decoder_debias,model:,help
OPTS=$(getopt -a -n debias --options $SHORT --longoptions $LONG -- "$@")

eval set -- "$OPTS"

collect_embedding_table=""
preprocess=""
translate=""
debias_encoder=""
begining_decoder_debias=""
end_decoder_debias=""
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
    -d | --debias_encoder )
      debias_encoder="-e"
      shift 1
      ;;
    -b | --begining_decoder_debias )
      begining_decoder_debias="-ds"
      shift 1
      ;;
    -e | --end_decoder_debias )
      end_decoder_debias="-de"
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
  -e, --debias_encoder            debias the encoder .
  -ds --begining_decoder_debias   debias the decoder inputs .
  -de --end_decoder_debias        debias the decoder outputs .
  -h, --help                      help message .
if none of debias_encoder, begining_decoder_debias, end_decoder_debias is selected, debias_encoder is selected defaultly"

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