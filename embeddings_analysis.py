import sys
import matplotlib.pyplot as plt
from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

WORDS_ASSIGNED_PATH = "TRAITEMENT/MODEL/words_assigned.txt"
MODEL_PATH = "TRAITEMENT/SAMPLES/CLEANED/models2/2000.txt.tt.formes.model"
RESULT_PATH = "TRAITEMENT/MODEL/result.txt"

def find_names(lines):
    pairs = []
    for line in lines[1:]:
        pair = line.split("\t")[0].split(", ")
        pairs.append((pair[0],pair[1]))
    return pairs

def find_adjs(lines):
    pairs = []
    for line in lines[1:]:
        pair = line.split("\t")
        pairs.append((pair[0],pair[1]))
    return pairs

def write_vocab(vocab):
    if vocab is not None:
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


def find_sim(model, complete_key):
    # Source :
    # https://radimrehurek.com/gensim/models/word2vec.html
    vector = model.wv[complete_key]
    # get other similar words
    sims = model.wv.most_similar(complete_key, topn=10)
    f = open(RESULT_PATH, "a")
    f.write("\n"+complete_key+" :")
    #~mots utilisés dans un contexte similaire au mot cible
    for sim in sims:
        f.write(sim[0]+',')
    f.close()
    return sims


def calculate_distance(model, complete_key_masc,complete_key_fem):
    dist = model.wv.similarity(complete_key_masc,complete_key_fem)
    f = open("result.txt", "a")
    f.write('\ndistance:'+str(dist)+'\n')
    f.close()
    return dist


def get_score_sim(model, complete_key_masc,complete_key_fem):
    sims_m = set([s[0] for s in find_sim(model, complete_key_masc)])
    sims_f = [s[0] for s in find_sim(model, complete_key_fem)]
    score = 0
    for sim_f in sims_f:
        if sim_f in sims_m:
            score += 1
    return score

def process_pairs(model, pairs, vocab):
    nb_paires = 0
    dist_tab=[]
    score_sim_tab=[]
    for pair in pairs:
        key_masc = pair[0]
        key_fem = pair[1]

        complete_key_masc = find_cat_key(key_masc,vocab)
        complete_key_fem = find_cat_key(key_fem,vocab)


        if complete_key_masc is not None and complete_key_fem is not None:
            score_sim = get_score_sim(model, complete_key_masc, complete_key_fem)
            dist = calculate_distance(model, complete_key_masc,complete_key_fem)
            nb_paires += 1
            dist_tab.append(dist)
            score_sim_tab.append(score_sim)

    print("nb_paires:",nb_paires)
    dist_avg = sum(dist_tab)/len(dist_tab)
    print("distance moyenne:", dist_avg)
    dist_avg = sum(score_sim_tab)/len(score_sim_tab)
    print("score sim moyen:",dist_avg)

def compare_model(comparing_model):
    pass

def main():
    # examples of command used to call this program :
    # python embeddings_analysis.py words_assigned.txt 2000.txt.tt.formes.model
    # python embeddings_analysis.py paires-adjs.txt 2000.txt.tt.formes.model
    # src_repere = sys.argv[1]
    # model_name = sys.argv[2]
    src_repere = WORDS_ASSIGNED_PATH
    lines_repere = open(src_repere, "r").read().splitlines()



    model_name = MODEL_PATH
    model = Word2Vec.load(model_name)
    vocab = model.wv.index_to_key
    write_vocab(vocab)
    # appel de fonctions pour étudier des paires de noms
    process_pairs(model, find_names(lines_repere), vocab)
    # appel de fonctions pour étudier des paires d'adjectifs
    #process_pairs(model, find_adjs(lines_repere), vocab)



if __name__ == '__main__':
    main()
