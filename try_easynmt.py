from easynmt import EasyNMT
from sacrebleu.metrics import BLEU
from detokenize import detokenize_matrix
import sys
# sys.path.append("../../") # Adds higher directory to python modules path.
sys.path.append("../../debias_manager") # Adds higher directory to python modules path.
from consts import get_debias_files_from_config, EMBEDDING_SIZE, DEFINITIONAL_FILE, PROFESSIONS_FILE, \
    GENDER_SPECIFIC_FILE, EQUALIZE_FILE, get_basic_configurations, DebiasMethod, DEBIAS_MANAGER_HOME
model = EasyNMT('opus-mt')
GOLD_HOME = "/cs/snapless/oabend/borgr/SSMT/data/"
ru_data = GOLD_HOME + "en_ru/newstest2019-enru.en"
de_data = GOLD_HOME + "en_de/newstest2012.en"
he_data = GOLD_HOME + "en_he/dev.en"

ru_gold = GOLD_HOME + "en_ru/newstest2019-enru.ru"
de_gold = GOLD_HOME + "en_de/newstest2012.de"
he_gold = GOLD_HOME + "en_he/dev.he"

ru_translation_file = DEBIAS_MANAGER_HOME + "en_ru_easynmt"
de_translation_file = DEBIAS_MANAGER_HOME + "en_de_easynmt"
he_translation_file = DEBIAS_MANAGER_HOME + "en_he_easynmt"
def check_easynmt():

    # #Translate several sentences to German
    # sentences = ['You can define a list with sentences.',
    #              'All sentences are translated to your target language.',
    #              'Note, you could also mix the languages of the sentences.']
    bleu = BLEU()
    with open(ru_data, 'r') as ru, open(de_data, 'r') as de, open(he_data, 'r') as he, \
        open(ru_gold, 'r') as ru_translation_gold, open(de_gold, 'r') as de_translation_gold, open(he_gold, 'r') as he_translation_gold,\
        open(ru_translation_file, 'w') as ru_translation_file_f, open(de_translation_file, 'w') as de_translation_file_f, open(he_translation_file, 'w') as he_translation_file_f:

        # print("translating he")
        # he_translation = model.translate(he.readlines(), source_lang='en', target_lang='he', show_progress_bar=True)
        # print(he_translation)
        # he_translation_file_f.writelines(he_translation)
        # print("he")
        # print(bleu.corpus_score(detokenize_matrix(he_translation,'he'), [detokenize_matrix(he_translation_gold.readlines(),'he')]))
        print("translating ru")
        ru_translation = model.translate(ru.readlines(), source_lang='en', target_lang='ru', show_progress_bar=True)
        ru_translation_file_f.writelines(ru_translation)
        print("ru")
        print(bleu.corpus_score(detokenize_matrix(ru_translation,'ru'), [detokenize_matrix(ru_translation_gold.readlines(), 'ru')]))
        print("translating de")
        de_translation = model.translate(de.readlines(), source_lang='en', target_lang='de', show_progress_bar=True)
        de_translation_file_f.writelines(de_translation)
        print("de")
        print(bleu.corpus_score(detokenize_matrix(de_translation,'de'), [detokenize_matrix(de_translation_gold.readlines(),'de')]))


if __name__ == '__main__':
    check_easynmt()