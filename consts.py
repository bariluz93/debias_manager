import json
import ast
#
# if __name__ == '__main__':
#     CONSTS_CONFIG = {"USE_DEBIASED":0, "LANGUAGE":0, "COLLECT_EMBEDDING_TABLE":0}
#     j =json.dumps(CONSTS_CONFIG)
#     with open("/cs/labs/gabis/bareluz/nematus_clean/nematus/consts_config.json","w") as f:
#         f.write(j)
from enum import Enum
from datetime import datetime

class Language(Enum):
    RUSSIAN = 0
    GERMAN = 1
    HEBREW = 2

TranslationModels =["NEMATUS","EASY_NMT"]
class TranslationModelsEnum(Enum):
    NEMATUS = 0
    EASY_NMT = 1
LANGUAGE_STR_TO_INT_MAP = {'ru': 0,'de':1,'he':2}
LANGUAGE_STR_MAP = {Language.RUSSIAN: "ru", Language.GERMAN: "de", Language.HEBREW: "he"}


class DebiasMethod(Enum):
    BOLUKBASY = 0
    NULL_IT_OUT = 1


EMBEDDING_SIZE = 256
PROJECT_HOME = "/cs/labs/gabis/bareluz/nematus_clean/"
NEMATUS_HOME = "/cs/labs/gabis/bareluz/nematus_clean/nematus/"
DEBIAS_FILES_HOME = "/cs/usr/bareluz/gabi_labs/nematus_clean/debias_files/"
PREPROCESS_HOME = "/cs/snapless/oabend/borgr/SSMT/preprocess/data/"
MT_GENDER_HOME = "/cs/usr/bareluz/gabi_labs/nematus_clean/mt_gender/"
DATA_HOME = "/cs/snapless/gabis/bareluz/data/"
OUTPUTS_HOME = "/cs/usr/bareluz/gabi_labs/nematus_clean/debias_outputs/"
param_dict = {
    Language.RUSSIAN:
        {
            "DICT_SIZE": 30648,
            "ENG_DICT_FILE": DATA_HOME + "en_ru_30.11.20//train.clean.unesc.tok.tc.bpe.en.json",
            "BLEU_SOURCE_DATA": DATA_HOME + "en_ru_30.11.20/newstest2019-enru.unesc.tok.tc.bpe.en",
            "BLEU_GOLD_DATA": DATA_HOME + "en_ru_30.11.20/newstest2019-enru.unesc.tok.tc.bpe.ru",

        },
    Language.GERMAN:
        {
            "DICT_SIZE": 29344,
            "ENG_DICT_FILE": DATA_HOME + "en_de_5.8/train.clean.unesc.tok.tc.bpe.en.json",
            "BLEU_SOURCE_DATA": DATA_HOME + "en_de_5.8/newstest2012.unesc.tok.tc.bpe.en",
            "BLEU_GOLD_DATA": DATA_HOME + "en_de_5.8/newstest2012.unesc.tok.tc.bpe.de",
        },
    Language.HEBREW:
        {
            "DICT_SIZE": 30545,
            "ENG_DICT_FILE": DATA_HOME + "en_he_20.07.21//train.clean.unesc.tok.tc.bpe.en.json",
            "BLEU_SOURCE_DATA": DATA_HOME + "en_he_20.07.21//dev.unesc.tok.tc.bpe.en",
            "BLEU_GOLD_DATA": DATA_HOME + "en_he_20.07.21//dev.unesc.tok.bpe.he",
        }
}


def parse_config(config_str):
    return ast.literal_eval(config_str)


def get_basic_configurations(config_str):
    config = parse_config(config_str)
    USE_DEBIASED = config["USE_DEBIASED"]
    LANGUAGE = config["LANGUAGE"]
    if "COLLECT_EMBEDDING_TABLE" in config.keys():
        COLLECT_EMBEDDING_TABLE = config["COLLECT_EMBEDDING_TABLE"]
    else:
        COLLECT_EMBEDDING_TABLE = None
    DEBIAS_METHOD = config["DEBIAS_METHOD"]
    TRANSLATION_MODEL = config["TRANSLATION_MODEL"]

    return USE_DEBIASED, LANGUAGE, COLLECT_EMBEDDING_TABLE, DEBIAS_METHOD, TRANSLATION_MODEL


def get_debias_files_from_config(config_str):
    config = parse_config(config_str)
    lang = LANGUAGE_STR_MAP[Language(config['LANGUAGE'])]
    debias_method = str(config['DEBIAS_METHOD'])
    translation_model = TranslationModels[int(config['TRANSLATION_MODEL'])]

    DICT_SIZE = param_dict[Language(int(config['LANGUAGE']))]["DICT_SIZE"]

    # the source english dictionary
    ENG_DICT_FILE = param_dict[Language(int(config['LANGUAGE']))]["ENG_DICT_FILE"]

    # the path of the file that translate wrote the embedding table to. this file will be parsed and debiased
    OUTPUT_TRANSLATE_FILE = OUTPUTS_HOME + "en-" + lang + "/debias/output_translate_" + lang + ".txt"

    # the file to which the initial embedding table is pickled to after parsing the file written when running translate
    EMBEDDING_TABLE_FILE = OUTPUTS_HOME + "en-" + lang + "/debias/embedding_table_" + lang + ".bin"

    # the file to which the initial (non debiased) embedding is written in the format of [word] [embedding]\n which is the format debiaswe uses. this is ready to be debiased
    EMBEDDING_DEBIASWE_FILE = OUTPUTS_HOME + "en-" + lang + "/debias/embedding_debiaswe_" + lang +"_"+translation_model+ ".txt"

    # the file to which the debiased embedding table is saved at the end
    DEBIASED_EMBEDDING = OUTPUTS_HOME + "en-" + lang + "/debias/Nematus-hard-debiased-" + lang + "-" + debias_method +"-"+translation_model+ ".txt"

    now = datetime.now()
    SANITY_CHECK_FILE = OUTPUTS_HOME + "en-" + lang + "/debias/sanity_check_" + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv"

    return DICT_SIZE, ENG_DICT_FILE, OUTPUT_TRANSLATE_FILE, EMBEDDING_TABLE_FILE, EMBEDDING_DEBIASWE_FILE, DEBIASED_EMBEDDING, SANITY_CHECK_FILE


def get_evaluate_gender_files(config_str):
    config = parse_config(config_str)
    lang = LANGUAGE_STR_MAP[Language(config['LANGUAGE'])]
    debias_method = str(config['DEBIAS_METHOD'])
    translation_model = TranslationModels[int(config['TRANSLATION_MODEL'])]

    # the translations of anti sentences, using the debiased embedding table, with source line nums printed
    ANTI_TRANSLATED_DEBIASED = OUTPUTS_HOME + "en-" + lang + "/output/debiased_anti_" + debias_method +"_"+translation_model+ ".out.tmp"

    # the translations of anti sentences, using the non debiased embedding table, with source line nums printed
    ANTI_TRANSLATED_NON_DEBIASED = OUTPUTS_HOME + "en-" + lang + "/output/non_debiased_anti_" + debias_method +"_"+translation_model+ ".out.tmp"


    # the full anti sentences in english (in the format <gender> <profession location> <sentence> <profession>)
    EN_ANTI_MT_GENDER = MT_GENDER_HOME + "data/aggregates/en_anti.txt"
    # the full sentences in english (in the format <gender> <profession location> <sentence> <profession>)
    EN_NEUTRAL_MT_GENDER = MT_GENDER_HOME + "data/aggregates/en.txt"


    # file prepared to evaluation in the form of source_sentence ||| translated_sentence. translated using debiased embedding table
    DEBIASED_EVAL = MT_GENDER_HOME + "translations/nematus/en-" + lang + "-debiased-"+debias_method +"_"+translation_model+".txt"

    # file prepared to evaluation in the form of source_sentence ||| translated_sentence. translated using non debiased embedding table
    NON_DEBIASED_EVAL = MT_GENDER_HOME + "translations/nematus//en-" + lang + "-non-debiased-"+debias_method +"_"+translation_model+".txt"



    return ANTI_TRANSLATED_DEBIASED, ANTI_TRANSLATED_NON_DEBIASED, DEBIASED_EVAL, NON_DEBIASED_EVAL, EN_ANTI_MT_GENDER, EN_NEUTRAL_MT_GENDER


def get_evaluate_translation_files(config_str):
    config = parse_config(config_str)
    lang = LANGUAGE_STR_MAP[Language(config['LANGUAGE'])]
    debias_method = str(config['DEBIAS_METHOD'])
    translation_model = TranslationModels[int(config['TRANSLATION_MODEL'])]

    # data of sentences for Bleu evaluation
    BLEU_SOURCE_DATA = param_dict[Language(int(config['LANGUAGE']))]["BLEU_SOURCE_DATA"]

    # data of the gold translation sentences for Bleu evaluation
    BLEU_GOLD_DATA = param_dict[Language(int(config['LANGUAGE']))]["BLEU_GOLD_DATA"]

    # the translations of the dataset sentences, using the debiased embedding table, with source line nums printed
    TRANSLATED_DEBIASED = OUTPUTS_HOME + "en-" + lang + "/output/debiased_" + debias_method + "_"+translation_model+".out.tmp"

    # the translations of the dataset sentences, using the non debiased embedding table, with source line nums printed
    TRANSLATED_NON_DEBIASED = OUTPUTS_HOME + "en-" + lang + "/output/non_debiased_" + debias_method +"_"+translation_model+ ".out.tmp"

    return BLEU_SOURCE_DATA, BLEU_GOLD_DATA, TRANSLATED_DEBIASED, TRANSLATED_NON_DEBIASED


#################debiaswe files#################
DEFINITIONAL_FILE = PROJECT_HOME + "debiaswe/data/definitional_pairs.json"
GENDER_SPECIFIC_FILE = PROJECT_HOME + "debiaswe/data/gender_specific_full.json"
PROFESSIONS_FILE = PROJECT_HOME + "debiaswe/data/professions.json"
EQUALIZE_FILE = PROJECT_HOME + "debiaswe/data/equalize_pairs.json"
