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

def word_in_vocab(key,vocab):
    if key+'_NOM' in vocab:
        return key_masc+'_NOM'
    elif key+'_ADJ' in vocab:
        return key_masc+'_ADJ'
    else:
        return None


def analyze_vector(model, complete_key):
    # Source :
    # https://radimrehurek.com/gensim/models/word2vec.html
    vector = model.wv[complete_key]
    # get other similar words
    sims = model.wv.most_similar(complete_key, topn=10)
    f = open("result.txt", "a")
    f.write(complete_key+" :")
    #~mots utilisés dans un contexte similaire au mot cible
    for sim in sims:
        f.write(sim[0]+',')
    f.write('\n\n')
    f.close()


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
    model = Word2Vec.load(model_name)

    # experimenting with model
    len_model = len(model.wv)

    vocab = model.wv.index_to_key
    write_vocab(False)

    for pair in pairs:
        key_masc = pair[0]
        key_fem = pair[1]

        if word_in_vocab(key_masc,vocab) is not Null:
            sims_masc = analyze_vector(model,)

        if key_masc+'_NOM' in vocab:
            sims_masc = analyze_vector(model, key_masc+'_NOM')
        elif key_masc+'_ADJ' in vocab:
            sims_masc = analyze_vector(model, key_masc+'_ADJ')

        if key_fem+'_NOM' in vocab:
            sims_fem = analyze_vector(model, key_fem+'_NOM')
        elif key_fem+'_ADJ' in vocab:
            sims_fem = analyze_vector(model, key_fem+'_ADJ')


if __name__ == '__main__':
    main()
