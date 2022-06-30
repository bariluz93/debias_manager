#!/bin/bash
set -e
#SBATCH --mem=128g
#SBATCH -c4
#SBATCH --time=7-0
#SBATCH --mail-type=BEGIN,END,FAIL,TIME_LIMIT
#SBATCH --mail-user=bar.iluz@mail.huji.ac.il
#SBATCH --output=/cs/usr/bareluz/gabi_labs/nematus_clean/nematus/slurm/evaluate_gender_bias-%j.out
echo "**************************************** in evaluate_gender_bias.sh ****************************************"

SHORT=l:,d:,t,a,b,e,h
LONG=language:,debias_method:,translate,debias_encoder,beginning_decoder_debias,end_decoder_debias,help
OPTS=$(getopt -a -n debias --options $SHORT --longoptions $LONG -- "$@")

eval set -- "$OPTS"

translate=false
debias_encoder=0
beginning_decoder_debias=0
end_decoder_debias=0
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
    -t | --translate )
      translate=true
      shift 1
      ;;
    -a | --debias_encoder )
      debias_encoder=1
      shift 1
      ;;
    -b | --beginning_decoder_debias )
      beginning_decoder_debias=1
      shift 1
      ;;
    -e | --end_decoder_debias )
      end_decoder_debias=1
      shift 1
      ;;
    -h | --help)
      echo "usage:
Mandatory arguments:
  -l, --language                  the destination translation language .
  -d, --debias_method             the debias method .
Optional arguments:
  -p, --preprocess                preprocess the anti dataset .
  -t, --translate                 translate the entire dataset .
  -a, --debias_encoder            debias the encoder .
  -b, --beginning_decoder_debias  debias the decoder inputs .
  -e, --end_decoder_debias        debias the decoder outputs .
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

scripts_dir=`pwd`
source ${scripts_dir}/consts.sh ${language} ${debias_method} 0

############preprocess###############
if [ $preprocess = true ]; then
  echo "#################### preprocess ####################"
  sh ${debias_files_dir}/global_preprocess.sh ${dst_language}
fi


#################### translate anti sentences to test gender bias ####################
input_path=${snapless_data_dir}/anti_data/${language_dir}/anti.unesc.tok.tc.bpe.en
#echo "input_path: ${input_path}"
model_type=bpe256
model_name=model.npz
model_dir=${snapless_data_dir}/models/${language_dir}/${model_type}/${model_name}
#echo "model_dir: ${model_dir}"
#output_filename_debiased=debiased_anti_TEST.out.tmp
outputh_path_debiased=${debias_outputs_dir}/${language_dir}/output/debiased_anti_${debias_method}_NEMATUS.out.tmp
outputh_path_non_debiased=${debias_outputs_dir}/${language_dir}/output/non_debiased_anti_${debias_method}_NEMATUS.out.tmp
#echo "outputh_path_debiased: ${outputh_path_debiased}"
#echo "outputh_path_non_debiased: ${outputh_path_non_debiased}"
config_debiased="{'USE_DEBIASED': 1, 'LANGUAGE': ${language_num}, 'COLLECT_EMBEDDING_TABLE': 0, 'DEBIAS_METHOD': ${debias_method}, 'TRANSLATION_MODEL': 0, 'DEBIAS_ENCODER': ${DEBIAS_ENCODER}, 'BEGINNING_DECODER_DEBIAS': ${beginning_decoder_debias}, 'END_DECODER_DEBIAS': ${end_decoder_debias}"
#echo "config_debiased: ${config_debiased}"
config_non_debiased="{'USE_DEBIASED': 0, 'LANGUAGE': ${language_num}, 'COLLECT_EMBEDDING_TABLE': 0, 'DEBIAS_METHOD': ${debias_method}, 'TRANSLATION_MODEL': 0, 'DEBIAS_ENCODER': ${DEBIAS_ENCODER}, 'BEGINNING_DECODER_DEBIAS': ${beginning_decoder_debias}, 'END_DECODER_DEBIAS': ${end_decoder_debias}}"

if [ $translate = true ]; then
  echo "#################### translate anti debias ####################"
  echo "python ${nematus_dir}/nematus/translate.py -i ${input_path} -m ${model_dir} -k 12 -n -o ${outputh_path_debiased} -c ${config_debiased}"
  python ${nematus_dir}/nematus/translate.py \
       -i "$input_path" \
       -m "$model_dir" \
       -k 12 -n -o "${outputh_path_debiased}" -c "${config_debiased}"
  echo "#################### translate anti non debias ####################"
  python ${nematus_dir}/nematus/translate.py \
       -i "$input_path" \
       -m "$model_dir" \
       -k 12 -n -o "${outputh_path_non_debiased}" -c "${config_non_debiased}"
fi


#echo "#################### merge translations ####################"
#python ${nematus_dir}/merge_translations.py \
#     -c "{'USE_DEBIASED': 0, 'LANGUAGE': ${language_num}, 'COLLECT_EMBEDDING_TABLE': 0, 'DEBIAS_METHOD': ${debias_method}}" \
#     -e 0
echo "#################### prepare gender data ####################"
python ${debias_files_dir}/prepare_gender_data.py  -c "${config_non_debiased}"

echo "#################### gender evaluation ####################"
output_result_path=${debias_outputs_dir}/${language_dir}/debias/gender_evaluation_${dst_language}_${debias_method}_${model_str}.txt
exec > ${output_result_path}
exec 2>&1
cd ${mt_gender_dir}
source venv/bin/activate
cd src
export FAST_ALIGN_BASE=/cs/usr/bareluz/gabi_labs/nematus_clean/nematus/fast_align
./../scripts/evaluate_language.sh ../data/aggregates/en_anti.txt ${language} ${model_str} ${debias_method}
#sh ../scripts/evaluate_debiased.sh ${language} ${debias_method} ${model_str}




