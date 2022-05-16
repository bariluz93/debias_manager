import argparse
from easynmt import EasyNMT
from consts import get_basic_configurations, LANGUAGE_STR_MAP, Language
model = EasyNMT('opus-mt')
# ru_data = DATA_HOME + "en_ru_30.11.20/newstest2019-enru.en"
# de_data = DATA_HOME + "en_de_5.8/newstest2012.en"
# he_data = DATA_HOME + "en_he_20.07.21/dev.en"
#
# ru_gold = DATA_HOME + "en_ru_30.11.20/newstest2019-enru.ru"
# de_gold = DATA_HOME + "en_de_5.8/newstest2012.de"
# he_gold = DATA_HOME + "en_he_20.07.21/dev.he"
#
# ru_translation_file = DEBIAS_FILES_HOME + "en_ru_easynmt.txt"
# de_translation_file = DEBIAS_FILES_HOME + "en_de_easynmt.txt"
# he_translation_file = DEBIAS_FILES_HOME + "en_he_easynmt.txt"

# def main():
#
#     bleu = BLEU()
#     with open(ru_data, 'r') as ru, open(de_data, 'r') as de, open(he_data, 'r') as he, \
#         open(ru_gold, 'r') as ru_translation_gold, open(de_gold, 'r') as de_translation_gold, open(he_gold, 'r') as he_translation_gold,\
#         open(ru_translation_file, 'w') as ru_translation_file_f, open(de_translation_file, 'w') as de_translation_file_f, open(he_translation_file, 'w') as he_translation_file_f:
#
#         print("translating he")
#         he_translation = model.translate(he.readlines(), source_lang='en', target_lang='he', show_progress_bar=True)
#         print(he_translation)
#         he_translation_file_f.writelines(he_translation)
#         print("he")
#         print(bleu.corpus_score(detokenize_matrix(he_translation,'he'), [detokenize_matrix(he_translation_gold.readlines(),'he')]))
#         print("translating ru")
#         ru_translation = model.translate(ru.readlines(), source_lang='en', target_lang='ru', show_progress_bar=True)
#         ru_translation_file_f.writelines(ru_translation)
#         print("ru")
#         print(bleu.corpus_score(detokenize_matrix(ru_translation,'ru'), [detokenize_matrix(ru_translation_gold.readlines(), 'ru')]))
#         print("translating de")
#         de_translation = model.translate(de.readlines(), source_lang='en', target_lang='de', show_progress_bar=True)
#         de_translation_file_f.writelines(de_translation)
#         print("de")
#         print(bleu.corpus_score(detokenize_matrix(de_translation,'de'), [detokenize_matrix(de_translation_gold.readlines(),'de')]))

def translate(input_file:str, output_file:str, config:str):
    USE_DEBIASED, LANGUAGE, _, DEBIAS_METHOD, _ = get_basic_configurations(config)
    with open(input_file, 'r') as input, open(output_file, 'w') as output:
        translations = model.translate(input.readlines(), source_lang='en', target_lang=LANGUAGE_STR_MAP[Language(LANGUAGE)], show_progress_bar=True, use_debiased = USE_DEBIASED)
        output.writelines(translations)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', type=argparse.FileType('r'),
        help="input file")
    parser.add_argument(
        '-o', '--output', type=argparse.FileType('r'),
        help="output file")
    parser.add_argument(
        '-c', '--config_str', type=str, required=True,
        help="a config dictionary str that conatains: \n"
             "USE_DEBIASED= run translate on the debiased dictionary or not\n"
             "LANGUAGE= the language to translate to from english. RUSSIAN = 0, GERMAN = 1, HEBREW = 2\n"
             "DEBIAS_METHOD= the debias method. BOLUKBASY = 0 NULL_IT_OUT = 1\n"
    )
    args = parser.parse_args()
    translate(args.input, args.output, args.config_str)
