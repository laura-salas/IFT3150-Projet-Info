import sys
import pandas as pd
#import matplotlib.pyplot as plt
from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from lemmatizer import lemmatize
from collections import Counter
#TODO : fix import
#from nltk.stem.snowball import SnowballStemmer

# PATHS #
# Contains the reference words along with their POS and other info about each of them
WORDS_ASSIGNED_PATH = "TRAITEMENT/MODEL/words_assigned.txt"
# The path to the current Gensym model
MODEL_PATH = "TRAITEMENT/SAMPLES/CLEANED/models2/2000.txt.tt.formes.model"
# The output paths
RESULT_PATH = "TRAITEMENT/MODEL/result.txt"

# Note, the paths below require the format to be specified like so:
# PAIRS_PATH % "txt" , or PAIRS_PATH % "csv", etc
PAIRS_PATH = "TRAITEMENT/MODEL/result_pairs.%s"
NEIGHBORS_PATH = "TRAITEMENT/MODEL/result_neighbours.%s"
SIMILARITIES_PATH = "TRAITEMENT/MODEL/result_distances.%s"
FREQUENCIES_PATH = "TRAITEMENT/MODEL/result_frequences.%s"
NEIGHBOURS_FREQUENCIES_PATH = "TRAITEMENT/MODEL/result_neighbours_frequences.%s"
PUR_SIM_PATH = "TRAITEMENT/MODEL/result_sim_pure.%s"
LEM_SIM_PATH = "TRAITEMENT/MODEL/result_sim_lemm.%s"
STE_SIM_PATH = "TRAITEMENT/MODEL/result_sim_stem.%s"
CALCULATED_BIAS_OUTPUT_PATH = "TRAITEMENT/MODEL/result_calculated_bias.%s"
CALCULATED_BIAS_PATH = "TRAITEMENT/MODEL/result_calculated_bias.json"

# Sample vocabulary to provide
SAMPLE_VOCAB = "sample_vocab.txt"

VOCAB_N = 1000
SIMILAR_WORDS_TO_GET = 10

# NLTK stemmer
#TODO : fix import
#stemmer = SnowballStemmer(language='french')


class dataType:
    """
    Object to classify data
    """
    def __init__(self, name, headers, output_path):
        self.name = name
        self.headers = headers
        self.output_path = output_path
        self.content = []

    def add_data(self, new_data: [any]):
        self.content.append([line for line in new_data])

    def get_output(self):
        # each sub-array of output will be a line
        output = [self.headers]
        for data in self.content:
            new_line = []
            for item in data:
                new_line.append(item)
            output.append(new_line)
        return output

    def __str__(self):
        master_str = ""
        for line in self.get_output():
            currLine = ""
            for item in line:
                currLine += str(item) + "\t"
            master_str += currLine + "\n"
        return master_str

    def output_as_txt(self):
        master_str = str(self)
        write_file(self.output_path % "txt", master_str, "w")

    def output_as_json(self):
        jsonObject = []
        for line in self.get_output()[1:]:
            curr_item = {}
            for idx, item in enumerate(line):
                curr_item[self.headers[idx]] = item
            jsonObject.append(curr_item)
        output = json.dumps(jsonObject)

        write_file(self.output_path % "json", output, "w")

    def output_as_csv(self):
        """
        Note: CSVs follow the following convention
        "header1","header2",...
        "data1","data2",...
        """
        master_str = ""
        for line in self.get_output():
            currLine = ""
            for item in line:
                currLine += '"%s",' % item
            master_str += currLine + "\n"
        write_file(self.output_path % "csv", master_str, "w")

    def output_all(self):
        self.output_as_txt()
        self.output_as_csv()
        # self.output_as_json()


def write_file(file_name: str, content: str, mode="w") -> None:
    """
    Write string to a file

    :param file_name: file to write on
    :param content: the content (as a string)
    :param mode: Specifies the mode in which the file is opened, defaults to "w" if left empty
    """
    f = open(file_name, mode)
    f.write(content)
    f.close()


def find_nouns(text: [str]) -> [([str], [str])]:
    """
    Find nouns in the provided text

    :param text: the text to go through
    :return: a list of sets that contain the fem and masc nouns
    """
    return [(line.split("\t")[0].split(", ")[0],
             line.split("\t")[0].split(", ")[1])
            for line in text[1:]]


def find_adjectives(text: [str]) -> [(str, str)]:
    """
    Find adjectives in the provided text

    :param text: the text to go through
    :return: a list of sets that contain the fem and masc adjectives
    """
    return [(line.split("\t")[0],
             line.split("\t")[1])
            for line in text[1:]]


def write_vocab(vocab: [str] = None) -> None:
    """
    If found any vocab in the model, write it to file

    :param vocab: (optional) vocab from model
    :return:
    """

    write_file(RESULT_PATH, "", "w")

    write_file(SAMPLE_VOCAB,
               "".join(element + "\n" for element in vocab[:VOCAB_N]),
               "w") \
        if vocab is not None else ""


def assign_POS_key(key: str, vocab: str):
    """
    Find key in vocabulary and assign POS (either ADJ or NOM (noun))

    :param key: word to find
    :param vocab: vocabulary to look through
    :return: vocab word if found, along with its POS (format: word_POS)
    """
    return key + '_NOM' if key + '_NOM' in vocab \
        else key + '_ADJ' if key + '_ADJ' in vocab \
        else None

def lemme(word):
    lemme = ""
    # voir code assign_infos.py
    return lemme


def lemme(word):
    lemme = ""
    # voir code assign_infos.py
    return lemme


def find_similar_neighbours(model, word_key: str) -> (str, [str], int):
    """
    Find neighbours of similar words

    :param model: input WordVec model
    :param word_key: the word to search the neighbours for
    :return: search result, "The most similar entries as a `(keys, best_rows, scores)`
                    tuple."

    # Source :
    # https://radimrehurek.com/gensim/models/word2vec.html
    """
    # get neighbours
    similar_neighbours = model.wv.most_similar(word_key, topn=SIMILAR_WORDS_TO_GET)


    word_count = model.wv.get_vecattr(word_key, "count")

    write_file(RESULT_PATH, "\n" + word_key + " (f=" + str(word_count) + ") : ", "a")

    # words used in a similar context as the target
    write_file(RESULT_PATH, " ".join(
        sim[0] + " (f=" + str(model.wv.get_vecattr(sim[0], "count")) + ")," for sim in similar_neighbours), "a")

    similar_neighbours_info = (similar_neighbours, word_count, [str(model.wv.get_vecattr(sim[0], "count"))  for sim in similar_neighbours])
    return similar_neighbours_info


def calculate_similarity(model, word_key_masc: str, word_key_fem: str) -> [(str, int)]:
    """
    Calculate distance vector between masculine and feminine word
    (both words deriving same lemma)

    :param model: model to get the distance from
    :param word_key_masc: masculine word
    :param word_key_fem: feminine word
    :return: "If fileid is specified, just the score for the two ngrams; otherwise,
                 list of tuples of fileids and scores."
    """
    dist = model.wv.similarity(word_key_masc, word_key_fem)
    write_file(RESULT_PATH, '\ndistance:' + str(dist) + '\n\n', "a")
    return dist


def get_similarity_score(model, complete_key_masc, complete_key_fem,
                         pureSimScore, stemSimScore, lemSimScore, neighbours_,
                         word_frequencies, neighbours_frequencies,
                         pairNo):
    """
    Get the similarity score between the masculine and feminine of a word (sharing same
    root lemma)

    :param model:
    :param complete_key_masc:
    :param complete_key_fem:
    :return:
    """

    sims_m_info = [s for s in find_similar_neighbours(model, complete_key_masc)]
    sims_f_info = [s for s in find_similar_neighbours(model, complete_key_fem)]

    sims_m = [s[0] for s in sims_m_info[0]]
    sims_f = [s[0] for s in sims_f_info[0]]

    word_frequencies.add_data([pairNo, sims_m_info[1], sims_f_info[1]])
    neighbours_frequencies.add_data([pairNo, sims_m_info[2], sims_f_info[2]])
    neighbours_.add_data([pairNo, sims_m, sims_f])

    # score de similarité basé sur l'équivalence pure entre les sims_f et les sims_m
    scoreSimPure = sum([1 if sim_f in set(sims_m) else 0 for sim_f in sims_f])

    write_file(RESULT_PATH, '\n\nscore de similarité pure : ' + str(scoreSimPure), "a")
    pureSimScore.add_data([pairNo, scoreSimPure])

    scoreSimLemma = 0
    raw_sims_m = [sim_m.split("_")[0] for sim_m in sims_m]
    raw_sims_f = [sim_f.split("_")[0] for sim_f in sims_f]

    lemmas_sims_m = Counter(lemmatize(' '.join(raw_sims_m)))
    lemmas_sims_f = Counter(lemmatize(' '.join(raw_sims_f)))
    for lemma_sims_m in lemmas_sims_m.keys():
        # pour chaque lemme, s'il est présent dans les sets de lemmes de sims_m et de sims_f:
        if lemma_sims_m in lemmas_sims_f.keys():
            # examiner le nombre de sims_m/sims_f associés au lemme et prendre le plus petit des deux
            scoreSimLemma += min(lemmas_sims_m[lemma_sims_m], lemmas_sims_f[lemma_sims_m])

    write_file(RESULT_PATH, '\nscore de similarité lemmatisée : ' + str(scoreSimLemma), "a")
    lemSimScore.add_data([pairNo, scoreSimLemma])

    scoreSimStemmed = 0
    raw_sims_m = [sim_m.split("_")[0] for sim_m in sims_m]
    raw_sims_f = [sim_f.split("_")[0] for sim_f in sims_f]

    stemmed_sims_m = []
    stemmed_sims_f = []

    for sim_idx in range(len(raw_sims_m)):
        #TODO : fix nltk import
        '''
        a = raw_sims_m[sim_idx]
        b = stemmer.stem(a)
        stemmed_sims_m.append(stemmer.stem(raw_sims_m[sim_idx]))
        stemmed_sims_f.append(stemmer.stem(raw_sims_f[sim_idx]))
        '''
        #TODO : remove the two following lines and replace with lines above
        stemmed_sims_m.append(raw_sims_m[sim_idx])
        stemmed_sims_f.append(raw_sims_f[sim_idx])

    stemmed_sims_m = Counter(stemmed_sims_m)
    stemmed_sims_f = Counter(stemmed_sims_f)

    for stemmed_sim_m in stemmed_sims_m.keys():
        # pour chaque lemme, s'il est présent dans les sets de lemmes de sims_m et de sims_f:
        if stemmed_sim_m in stemmed_sims_f.keys():
            # examiner le nombre de sims_m/sims_f associés au lemme et prendre le plus petit des deux
            scoreSimStemmed += min(stemmed_sims_m[stemmed_sim_m], stemmed_sims_f[stemmed_sim_m])
    stemSimScore.add_data([pairNo, scoreSimStemmed])
    write_file(RESULT_PATH, '\nscore de similarité stemmed : ' + str(scoreSimStemmed), "a")

    return scoreSimPure


def process_pairs(model, pairs, vocab, pairs_,
                  pureSimScore_, stemSimScore_,
                  lemSimScore_, neighbours_, similarities_,
                  frequences_, neighbour_frequency_data_):
    """
    model
    :param pairs_:
    :param model:
    :param pairs:
    :param vocab:
    :return:
    """
    pairs_amount = 0
    # array of distances for each pair
    distances = []
    # array of simila
    # rity scores for each pair
    similarity_scores = []

    for pair in pairs:
        key_masc = pair[0]
        key_fem = pair[1]

        word_key_masc = assign_POS_key(key_masc, vocab)
        word_key_fem = assign_POS_key(key_fem, vocab)

        if word_key_masc is not None and word_key_fem is not None:
            pairs_.add_data([str(pairs_amount), str(key_fem), str(key_masc)])
            similarity_score = get_similarity_score(model, word_key_masc,
                                                    word_key_fem, pureSimScore_,
                                                    stemSimScore_, lemSimScore_,
                                                    neighbours_,
                                                    frequences_,
                                                    neighbour_frequency_data_,
                                                    pairs_amount)
            distance = calculate_similarity(model, word_key_masc, word_key_fem)

            distances.append(distance)
            similarities_.add_data([pairs_amount, distance])
            similarity_scores.append(similarity_score)
            pairs_amount += 1


def main():
    # OUR DATA TYPES
    pairs_ = dataType("paires", ["global_ref", "paire (f)", "paire (m)"], PAIRS_PATH)
    neighbours_ = dataType("voisins", ["ref_id", "voisins_m", "voisins_f"], NEIGHBORS_PATH)
    similarities_ = dataType("voisins", ["ref_id", "distance"], SIMILARITIES_PATH)
    pureSimScore_ = dataType("score similarité pure", ["ref_id", "score_sim_pure"], PUR_SIM_PATH)
    stemSimScore_ = dataType("score similarité stemmed", ["ref_id", "score_sim_stemm"], STE_SIM_PATH)
    lemSimScore_ = dataType("score similarité lemmatisée", ["ref_id", "score_sim_lemm"], LEM_SIM_PATH)
    nbOccurrences_ = dataType("score nombre d'ocurrance", ["ref_id", "frequence_m", "frequence_f", ], FREQUENCIES_PATH)
    neighbour_frequency_data = dataType("score frequences", ["ref_id", "neighbours_frequences_m",
                                                             "neighbours_frequences_f", ], NEIGHBOURS_FREQUENCIES_PATH)
    calculatedBias_ = dataType("calculated bias", ["ref_id", "bias (m)",
                                                             "bias (f)", ], CALCULATED_BIAS_OUTPUT_PATH)

    lines_reference = open(WORDS_ASSIGNED_PATH, "r").read().splitlines()

    calculated_bias = json.loads(open(CALCULATED_BIAS_PATH, "r").read())

    for idx, line in enumerate(calculated_bias):
        arr = []
        arr.append(idx)
        for key in line:
             arr.append(line[key])
        calculatedBias_.add_data(arr)

    model = Word2Vec.load(MODEL_PATH)
    vocab = model.wv.index_to_key
    write_vocab()

    # IMPORTANT : choisir la ligne appropriée selon étude de noms ou adj.s
    # appel de fonctions pour étudier des paires de noms
    process_pairs(model, find_nouns(lines_reference), vocab, pairs_,
                  pureSimScore_, stemSimScore_, lemSimScore_, neighbours_,
                  similarities_, nbOccurrences_, neighbour_frequency_data)

    # appel de fonctions pour étudier des paires d'adjectifs
    pairs_.output_all()
    pureSimScore_.output_as_json()
    neighbours_.output_all()
    pureSimScore_.output_all()
    stemSimScore_.output_all()
    lemSimScore_.output_all()
    similarities_.output_all()
    neighbours_.output_all()
    nbOccurrences_.output_all()
    neighbour_frequency_data.output_all()
    calculatedBias_.output_all()
    frequence_.output_all()
    neighbour_frequency_data_.output_all()

    df_pairs = pd.DataFrame(pairs_.get_output())
    df_pure_score = pd.DataFrame(pureSimScore_.get_output())
    df_lem_score = pd.DataFrame(lemSimScore_.get_output())
    df_stem_score = pd.DataFrame(stemSimScore_.get_output())

    scores_table = df_pairs.merge(df_pure_score).merge(df_lem_score).merge(df_stem_score)

    return scores_table


if __name__ == '__main__':
    main()
