# from datasets import load_dataset
# books = load_dataset("opus_books", "en-es")
# books = books["train"].train_test_split(test_size=0.2)
# with open("/cs/snapless/gabis/bareluz/data/en_es/books.en",'w') as english_file, open("/cs/snapless/gabis/bareluz/data/en_es/books.es",'w') as spanish_file:
#     for i in range(books.shape["train"][0]):
#         english_file.write(books["train"][i]['translation']['en']+"\n")
#         spanish_file.write(books["train"][i]['translation']['es']+"\n")
#     # for i in range(books.shape["test"][0]):
#     #     english_file.write(books["test"][i]['translation']['en'])
#     #     spanish_file.write(books["test"][i]['translation']['es'])

import argparse
from easynmt import EasyNMT
from consts import get_basic_configurations, LANGUAGE_STR_MAP, Language
model = EasyNMT('opus-mt')

def translate(input_file:str, output_file:str, config:str):
    USE_DEBIASED, LANGUAGE, _, DEBIAS_METHOD, _ ,_,_,_,_= get_basic_configurations(config)
    with open(input_file, 'r') as input, open(output_file, 'w') as output:
        translations = model.translate(input.readlines(), source_lang='en', target_lang=LANGUAGE_STR_MAP[Language(LANGUAGE)], show_progress_bar=True, use_debiased = USE_DEBIASED, debias_method=DEBIAS_METHOD)
        output.writelines(translations)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', type=str,
        help="input file")
    parser.add_argument(
        '-o', '--output', type=str,
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
