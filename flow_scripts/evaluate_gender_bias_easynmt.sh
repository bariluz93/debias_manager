#!/bin/bash
set -e
#SBATCH --mem=128g
#SBATCH -c4
#SBATCH --time=7-0
#SBATCH --mail-type=BEGIN,END,FAIL,TIME_LIMIT
#SBATCH --mail-user=bar.iluz@mail.huji.ac.il
#SBATCH --output=/cs/usr/bareluz/gabi_labs/nematus_clean/nematus/slurm/evaluate_gender_bias-%j.out
echo "**************************************** in evaluate_gender_bias.sh ****************************************"

SHORT=l:,d:,t,h
LONG=language:,debias_method:,translate,help
OPTS=$(getopt -a -n debias --options $SHORT --longoptions $LONG -- "$@")

eval set -- "$OPTS"

translate=false

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
    -h | --help)
      echo "usage:
Mandatory arguments:
  -l, --language                  the destination translation language .
  -d, --debias_method             the debias method .
Optional arguments:
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

scripts_dir=`pwd`
source ${scripts_dir}/consts.sh ${language} ${debias_method} 1



#################### translate anti sentences to test gender bias ####################
input_path=${snapless_data_dir}/anti_data/anti.en
outputh_path_debiased=${debias_outputs_dir}/${language_dir}/output/debiased_anti_${debias_method}_EASY_NMT.out.tmp
outputh_path_non_debiased=${debias_outputs_dir}/${language_dir}/output/non_debiased_anti_${debias_method}_EASY_NMT.out.tmp
config_debiased="{'USE_DEBIASED': 1, 'LANGUAGE': ${language_num}, 'DEBIAS_METHOD': ${debias_method}, 'TRANSLATION_MODEL': 1}"
config_non_debiased="{'USE_DEBIASED': 0, 'LANGUAGE': ${language_num}, 'DEBIAS_METHOD': ${debias_method}, 'TRANSLATION_MODEL': 1}"

if [ $translate = true ]; then
  echo "#################### translate anti debias ####################"
#  echo "python ${nematus_dir}/nematus/translate.py -i ${input_path} -m ${model_dir} -k 12 -n -o ${outputh_path_debiased} -c ${config_debiased}"
  python ${debias_files_dir}/translate_easynmt.py \
       -i "$input_path" \
       -o "${outputh_path_debiased}" \
       -c "${config_debiased}"
  echo "#################### translate anti non debias ####################"
#  echo "python ${nematus_dir}/nematus/translate.py -i ${input_path} -m ${model_dir} -k 12 -n -o ${outputh_path_non_debiased} -c ${config_non_debiased}"
  python ${debias_files_dir}/translate_easynmt.py \
       -i "$input_path" \
       -o "${outputh_path_non_debiased}" \
       -c "${config_non_debiased}"
fi


echo "#################### prepare gender data ####################"
python ${debias_files_dir}/prepare_gender_data.py  -c "${config_non_debiased}"

echo "#################### gender evaluation ####################"
output_result_path=${debias_outputs_dir}/${language_dir}/debias/gender_evaluation_${dst_language}_${debias_method}_${model_str}.txt
exec > ${output_result_path}
exec 2>&1
cd ${mt_gender_dir}
source venv/bin/activate
cd src
sh ../scripts/evaluate_debiased.sh ${language} ${debias_method}




