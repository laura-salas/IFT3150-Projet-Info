# Noms : Thalie St-Jacques et Laura Salas
# Date : 25-01-2022
# pseudocode pour l'instant
import pandas as pd

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

def lemmatize(word_pos):
    # Source : http://www.lexique.org/?page_id=76
    word_pos_tab = word_pos.split("_")
    word = word_pos_tab[0]
    pos = word_pos_tab[1]
    lex = pd.read_csv('http://www.lexique.org/databases/Lexique382/Lexique382.tsv', sep='\t')
    lex.head()
    word_infos = lex[(lex.ortho == word) & (lex.cgram==pos)]
    if word_infos.size == 1:
        #TODO : trouver comment accéder au lemme
        lemme = word_infos.lemme+pos
    else:
        lemme = word_pos
    return lemme



def main():

    src_path = ""
    #read_src(src_path)
    print(lemmatize('absentes_ADJ'))

    # pseudocode lemmatizer
    # lire input
    # pour chaque mot, regarder si dans la liste (liste Larreau)
        # si oui, pas lemmatiser
        # si non, lemmatiser
    # après avoir tout lu et traité le input, produire vecteurs
    # (pas une mince tâche tout de même)




if __name__ == '__main__':
    main()
