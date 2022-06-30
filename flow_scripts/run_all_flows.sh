#!/bin/bash
set -e
#SBATCH --mem=128g
#SBATCH -c4
#SBATCH --time=7-0
#SBATCH --mail-type=BEGIN,END,FAIL,TIME_LIMIT
#SBATCH --mail-user=bar.iluz@mail.huji.ac.il
#SBATCH --output=/cs/usr/bareluz/gabi_labs/nematus_clean/nematus/slurm/run_all_flows-%j.out

SHORT=l:,d:,c,p,t,a,b,e,m:,h
LONG=language:,debias_method:,collect_embedding_table,preprocess,translate,debias_encoder,beginning_decoder_debias,end_decoder_debias,model:,help
OPTS=$(getopt -a -n debias --options $SHORT --longoptions $LONG -- "$@")

eval set -- "$OPTS"

collect_embedding_table=false
preprocess=""
translate=""
debias_encoder=""
beginning_decoder_debias=""
end_decoder_debias=""
model=""
while :
do
  case "$1" in
    -l | --language )
      language="$2"
      shift 2
      ;;
    -d | --debias_method )
      debias_method="$2"
      shift 2
      ;;
    -c | --collect_embedding_table )
      collect_embedding_table=true
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
    -a | --debias_encoder )
      debias_encoder="-a"
      shift 1
      ;;
    -b | --beginning_decoder_debias )
      beginning_decoder_debias="-b"
      shift 1
      ;;
    -e | --end_decoder_debias )
      end_decoder_debias="-e"
      shift 1
      ;;
    -m | --model )
      model="$2"
      shift 2
      ;;
    -h | --help)
      echo "usage:
Mandatory arguments:
  -l, --language                  the destination translation language .
  -d, --debias_method             the debias method .
  -m, --model                     the translation model .
Optional arguments:
  -c, --collect_embedding_table   collect embedding table .
  -p, --preprocess                preprocess the anti dataset .
  -t, --translate                 translate the entire dataset .
  -a, --debias_encoder            debias the encoder .
  -b  --beginning_decoder_debias  debias the decoder inputs .
  -e, --end_decoder_debias        debias the decoder outputs .
  -h, --help                      help message .
if none of debias_encoder, beginning_decoder_debias, end_decoder_debias is selected, debias_encoder is selected defaultly"

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

if [ "$model" == "" ]; then
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
#echo "collect_embedding_table: ${collect_embedding_table},preprocess: ${preprocess},translate: ${translate}"

scripts_dir=`pwd`
source ${scripts_dir}/consts.sh ${language} ${debias_method} ${model}

if [ $collect_embedding_table = true ]; then
  sh print_embedding_table.sh ${language} ${debias_method}
fi

if [ "$model" == "0" ]; then
  echo "running nematus flows"
  sh evaluate_gender_bias.sh -l ${language} -d ${debias_method} ${preprocess} ${translate} ${debias_encoder} ${begining_decoder_debias} ${end_decoder_debias}
  sh evaluate_translation.sh -l ${language} -d ${debias_method} ${translate} ${debias_encoder} ${begining_decoder_debias} ${end_decoder_debias}
else
    echo "running easyNMT flows"
  sh evaluate_gender_bias_easynmt.sh -l ${language} -d ${debias_method} ${preprocess} ${translate} ${debias_encoder} ${begining_decoder_debias} ${end_decoder_debias}
  sh evaluate_translation_easynmt.sh -l ${language} -d ${debias_method} ${translate} ${debias_encoder} ${begining_decoder_debias} ${end_decoder_debias}
fi