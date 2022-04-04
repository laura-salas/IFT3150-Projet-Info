# Noms : Thalie St-Jacques et Laura Salas
# Date : 25-01-2022
import pandas as pd
import spacy

nlp = spacy.load("fr_core_news_sm")
lemmatizer = nlp.get_pipe("lemmatizer")

def read_src(src_path):
    lines = open(src_path, "r", encoding="utf-8").read().splitlines()
    treated_txt = []
    for line in lines:
        split_line = line.split("\t")
        word = line[0]
        if word in list:
            lemmatized_form = word.lower()
            line[2] = lemmatized_form
        treated_txt.append('\t'.join(split_line))

#TODO : améliorer le code car un peu redondant
def lex_lemmatize(word_pos):
    # Source : http://www.lexique.org/?page_id=76
    word_pos_tab = word_pos.split("_")
    word = word_pos_tab[0]
    pos = word_pos_tab[1]
    lex = pd.read_csv('http://www.lexique.org/databases/Lexique382/Lexique382.tsv', sep='\t')
    lex.head()
    lex = lex[['ortho','lemme','cgram']]
    word_infos = lex[(lex.ortho == word) & (lex.cgram==pos)]
    # produce lemma_pos
    if word_infos.shape[0]== 1:
        lemma_pos = word_infos.lemme.to_string(index=False)+"_"+pos
    else:
        lemma_pos = word_pos
    # produce lemma
    word_infos = lex[(lex.ortho == word)]
    if word_infos.shape[0]== 1:
        lemma = word_infos.lemme.to_string(index=False)
    else:
        lemma = word
    return (lemma_pos,lemma)


def lemmatize(words):
    tokens = nlp(words)
    lemmas = [token.lemma_ for token in tokens]
    return lemmas




def main():

    src_path = ""
    #read_src(src_path)

    # pseudocode lemmatizer
    # lire input
    # pour chaque mot, regarder si dans la liste (liste Larreau)
        # si oui, pas lemmatiser
        # si non, lemmatiser
    # après avoir tout lu et traité le input, produire vecteurs
    # (pas une mince tâche tout de même)
    # lemmatize("Je suis malade")
    lemmatize(["Je","suis","malade"])




if __name__ == '__main__':
    main()
