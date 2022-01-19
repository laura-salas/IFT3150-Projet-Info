# Noms : Thalie St-Jacques et Laura Salas
# Date : 16-01-2022

import pandas as pd

# ============== VARIABLES GLOBALES
# relative path
src_path = "Repertoire de paires\paires-Lareau.txt"

# ==============

def verify_order(pair):
    if len(pair[0])>=len(pair[1]):
        print("oh no!",pair)
    if pair[0][-1] == 'e':
        print("oh no!",pair)

def verify_categ(pair, noms, adjs):
    # regarder si le mot est listé comme adjectif et comme nom
    if pair[0] in noms.values() and pair[0] in adjs.values():
        print("adjectif qui est aussi un nom!", pair)

# =============

def main():

    lines = open(src_path, "r", encoding="utf-8").read().splitlines()

    # Source : http://www.lexique.org/?page_id=76
    lex = pd.read_csv('http://www.lexique.org/databases/Lexique382/Lexique382.tsv', sep='\t')

    # pas sure que cette ligne soit necessaire
    lex.head()

    noms = lex.loc[lex.cgram == 'NOM'].ortho.to_dict()
    adjs = lex.loc[lex.cgram == 'ADJ'].ortho.to_dict()
    print(noms.values())
    print(adjs)

    for line in lines:
        pair = line.split("\t")
        # Etape 1 : verifier la liste de mots qu'on a actuellement
        #verify_order(pair)
        verify_categ(pair, noms, adjs)


if __name__ == '__main__':
    main()
