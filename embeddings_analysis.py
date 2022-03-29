import sys
#import matplotlib.pyplot as plt
from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from lemmatizer.py import lemmatize

# PATHS #
# Contains the reference words along with their POS and other info about each of them
WORDS_ASSIGNED_PATH = "TRAITEMENT/MODEL/words_assigned.txt"
# The path to the current Gensym model
MODEL_PATH = "TRAITEMENT/SAMPLES/CLEANED/models2/2000.txt.tt.formes.model"
# The ouput path
RESULT_PATH = "TRAITEMENT/MODEL/result.txt"
# Sample vocabulary to provide
SAMPLE_VOCAB = "sample_vocab.txt"

# CONSTANTS #
VOCAB_N = 1000
SIMILAR_WORDS_TO_GET = 10


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

    # TODO: régler le bug de pourquoi ca réécrit par dessus le fichier si on re-roule le code\
    #  sans vider le fichier de result: peut-être le vider\
    #  a chaque fois?
    write_file(RESULT_PATH, "", "w")

    write_file(SAMPLE_VOCAB,
               "".join(element + "\n" for element in vocab[:VOCAB_N]),
               "w") \
        if vocab is not None else ""


def assign_POS_key(key: str, vocab: str):
    """
    Find key in vocabulary and assign POS (either ADJ or NOM (noun))
    #TODO: est-ce qu'on peut renommer NOM à NOUN?

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

    vector = model.wv[word_key]

    # get other similar words
    similar_neighbours = model.wv.most_similar(word_key, topn=SIMILAR_WORDS_TO_GET)
    # TODO: verifier si la frequence c'est le count ou le %
    word_count = model.wv.get_vecattr(word_key, "count")
    write_file(RESULT_PATH, "\n" + word_key +" (f="+str(word_count)+") : ", "a")

    # words used in a similar context as the target
    write_file(RESULT_PATH, " ".join(sim[0]+" (f="+str(model.wv.get_vecattr(sim[0], "count")) + ")," for sim in similar_neighbours), "a")

    return similar_neighbours


def calculate_distance(model, word_key_masc: str, word_key_fem: str) -> [(str, int)]:
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
    write_file(RESULT_PATH, '\ndistance:' + str(dist) + '\n', "a")
    return dist


def get_similarity_score(model, complete_key_masc, complete_key_fem):
    """
    Get the similarity score between the masculine and feminine of a word (sharing same
    root lemma)
    TODO: better define the similarity score and ask ourselves if this is the best method

    :param model:
    :param complete_key_masc:
    :param complete_key_fem:
    :return:
    """
    sims_m = set([s[0] for s in find_similar_neighbours(model, complete_key_masc)])
    sims_f = [s[0] for s in find_similar_neighbours(model, complete_key_fem)]

    # score de similarité basé sur l'équivalence pure entre les sims_f et les sims_m
    score1 = sum([1 if sim_f in sims_m else 0 for sim_f in sims_f])
    write_file(RESULT_PATH, '\n\nscore de similarité pure :' + str(score1) + '\n', "a")

    # score de similarité basé sur l'équivalence "lemmatique" entre les sims_f et les sims_m
    # pseudocode
    # faire un set de lemmes associés aux sims_m et un set de lemmes associés aux sims_f
    # TODO : finir lemmatizer
    lemmes_sims_m = [lemmatizer.lemmatize(sim_m) for sim_m in sims_m]
    # pour un lemme donné, si il est présent dans les sets de lemmes de sims_m et de sims_f
    # examiner le nombre de sims_m/sims_f associés au lemme et prendr le plus petit des deux

    score2 = 0
    write_file(RESULT_PATH, '\nscore de similarité lemmatisé :' + str(score2) + '\n', "a")

    return score


def process_pairs(model, pairs, vocab):
    """
    model
    :param model:
    :param pairs:
    :param vocab:
    :return:
    """
    pairs_amount = 0
    # array of distances for each pair
    distances = []
    # array of similarity scores for each pair
    similarity_scores = []

    for pair in pairs:
        key_masc = pair[0]
        key_fem = pair[1]

        word_key_masc = assign_POS_key(key_masc, vocab)
        word_key_fem = assign_POS_key(key_fem, vocab)

        # TODO : vérifier que les deux clés sont dans la meme POS aussi
        if word_key_masc is not None and word_key_fem is not None:
            # TODO : lemmatiser le key fem pour comparer le string avec le key masc

            similarity_score = get_similarity_score(model, word_key_masc, word_key_fem)
            distance = calculate_distance(model, word_key_masc, word_key_fem)
            pairs_amount += 1
            distances.append(distance)
            similarity_scores.append(similarity_score)

    print("pairs_amount:", pairs_amount)
    dist_avg = sum(distances) / len(distances)
    print("distance moyenne:", dist_avg)
    similarity_score_avg = sum(similarity_scores) / len(similarity_scores)
    print("score sim moyen:", similarity_score_avg)


def main():

    lines_reference = open(WORDS_ASSIGNED_PATH, "r").read().splitlines()

    model = Word2Vec.load(MODEL_PATH)
    vocab = model.wv.index_to_key
    write_vocab()
    # write_vocab(vocab)

    # IMPORTANT : choisir la ligne appropriée selon étude de noms ou adj.s
    # appel de fonctions pour étudier des paires de noms
    process_pairs(model, find_nouns(lines_reference), vocab)
    # appel de fonctions pour étudier des paires d'adjectifs
    # process_pairs(model, find_adjs(lines_reference), vocab)


if __name__ == '__main__':
    main()
