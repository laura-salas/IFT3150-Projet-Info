from gensim.test.utils import common_texts
from gensim.models import Word2Vec
import sys

def main():

    # example of command used to call this program :
    # python embeddings_analysis.py words_assigned.txt 2000.txt.tt.formes.model
    src_repere = sys.argv[1]

    lines = open(src_repere, "r").read().splitlines()
    pairs = []
    for line in lines[1:]:
        pair = line.split("\t")[0].split(",")
        print("pair:", pair)
        pairs.append((pair[0],pair[1]))


    model_name = sys.argv[2]
    # The model must be in the same dir as this .py
    model = Word2Vec.load(model_name)

    for pair in pairs:
        # Source :
        # https://radimrehurek.com/gensim/models/word2vec.html
        vector_masc = model.wv[pair[0]]
        vector_fem = model.wv[pair[1]]
        sims_masc = model.wv.most_similar(pair[0], topn=10)
        sims_fem = model.wv.most_similar(pair[1], topn=10)
        f = open("result.txt", "a")
        f.write(pair[0]+" : "+sims_masc)
        f.write(pair[1]+" : "+sims_fem)
        f.close()

if __name__ == '__main__':
    main()
