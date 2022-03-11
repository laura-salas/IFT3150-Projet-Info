from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import sys

def write_vocab(vocab_is_new):
    if vocab_is_new:
        textfile = open("sample_vocab.txt", "w")
        for element in vocab[:1000]:
            textfile.write(element + "\n")
        textfile.close()


def find_cat_key(key,vocab):
    if key+'_NOM' in vocab:
        return key+'_NOM'
    elif key+'_ADJ' in vocab:
        return key+'_ADJ'
    else:
        return None


def find_sim(complete_key):
    # Source :
    # https://radimrehurek.com/gensim/models/word2vec.html
    vector = model.wv[complete_key]
    # get other similar words
    sims = model.wv.most_similar(complete_key, topn=10)
    f = open("result.txt", "a")
    f.write("\n"+complete_key+" :")
    #~mots utilisés dans un contexte similaire au mot cible
    for sim in sims:
        f.write(sim[0]+',')
    f.close()


def calculate_distance(complete_key_masc,complete_key_fem):
    dist = model.wv.similarity(complete_key_masc,complete_key_fem)
    f = open("result.txt", "a")
    f.write('\ndistance:'+str(dist)+'\n')
    f.close()


def analyze_vector(complete_key_masc,complete_key_fem):
    find_sim(complete_key_masc)
    find_sim(complete_key_fem)
    distance_mf = calculate_distance(complete_key_masc,complete_key_fem)


def main():
    # example of command used to call this program :
    # python embeddings_analysis.py words_assigned.txt 2000.txt.tt.formes.model
    src_repere = sys.argv[1]

    lines = open(src_repere, "r").read().splitlines()
    pairs = []
    for line in lines[1:]:
        pair = line.split("\t")[0].split(", ")
        pairs.append((pair[0],pair[1]))


    model_name = sys.argv[2]
    # The model must be in the same dir as this .py
    global model
    model = Word2Vec.load(model_name)

    vocab = model.wv.index_to_key
    write_vocab(False)

    for pair in pairs:
        key_masc = pair[0]
        key_fem = pair[1]

        complete_key_masc = find_cat_key(key_masc,vocab)
        complete_key_fem = find_cat_key(key_fem,vocab)

        if complete_key_masc is not None and complete_key_fem is not None:
            analyze_vector(complete_key_masc, complete_key_fem)


if __name__ == '__main__':
    main()
