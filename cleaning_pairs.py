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
        return False
    elif pair[1] in noms.values() and pair[1] in adjs.values():
        print("adjectif qui est aussi un nom!", pair)
        return False
    else:
        return True

def create_adj_pairs(adjs):
    print("gf")

# =============

def main():


    lines = open(src_path, "r", encoding="utf-8").read().splitlines()

    # Source : http://www.lexique.org/?page_id=76
    lex = pd.read_csv('http://www.lexique.org/databases/Lexique382/Lexique382.tsv', sep='\t')

    # pas sure que cette ligne soit necessaire
    lex.head()
    '''
    noms = lex.loc[lex.cgram == 'NOM'].ortho.to_dict()
    adjs = lex.loc[lex.cgram == 'ADJ'].ortho.to_dict()
    print(noms.values())
    print(adjs)

    good_pairs = []

    for line in lines:
        pair = line.split("\t")
        # Etape 1 : verifier l'ordre (MASC,FEM)
        #verify_order(pair)
        # Etape 2 : verifier que le mot est seulement un nom
        if(verify_categ(pair, noms, adjs)):
            good_pairs.append(line)
    print("good_pairs:",good_pairs)


    f = open("paires-Lareau_cleaned.txt", "w")
    f.write('\n'.join(good_pairs))
    f.close()
    '''

    # Étape 3 : créer liste d'adjectifs réguliers
    # dans adjs, regarder categ cgramortho pour verifier que c'est JUSTE adj
    # trouver m, trouver f
    # append
    # write
    adjs_reg = lex.loc[(lex.cgram == 'ADJ')&(lex.cgramortho == 'ADJ')&(lex.genre == 'f') & (lex.nblettres <= 4)&(lex.nombre == 's')]
    for adj_reg in adjs_reg:
        line = adj_reg.lemme+"\t"+adj_reg.ortho
        adj_pairs.append(line)
    #adjs_reg = adjs_list.loc[(adjs_list.cgramortho == 'ADJ')&(adjs_list.genre == 'f')].ortho.to_dict()
    print(adjs_reg)
    f = open("paires-Lareau_cleaned.txt", "w")
    f.write('\n'.join(adj_pairs))
    f.close()


if __name__ == '__main__':
    main()
