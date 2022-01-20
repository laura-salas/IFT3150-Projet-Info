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
    # regarder si le mot est listé comme adjectif
    # on retourne False si le mot est
    # soit un adjectif, soit à la fois un nom et un adjectif
    if pair[0] in adjs.values() or pair[1] in adjs.values():
        print("nom qui est aussi un adjectif!", pair)
        return False
    else:
        return True

# =============

def main():


    lines = open(src_path, "r", encoding="utf-8").read().splitlines()

    # Source : http://www.lexique.org/?page_id=76
    lex = pd.read_csv('http://www.lexique.org/databases/Lexique382/Lexique382.tsv', sep='\t')

    # pas sure que cette ligne soit necessaire
    lex.head()

    noms = lex.loc[lex.cgram == 'NOM'].ortho.to_dict()
    adjs = lex.loc[lex.cgram == 'ADJ'].ortho.to_dict()

    good_pairs = []

    for line in lines:
        pair = line.split("\t")
        # Etape 1 : verifier l'ordre (MASC,FEM) : ok
        # le programme print les paires qui pourraient
        # etre problematiques
        verify_order(pair)
        # Etape 2 : verifier que le mot est seulement un nom
        if(verify_categ(pair, noms, adjs)):
            good_pairs.append(line)
    f = open("paires-Lareau_cleaned.txt", "w")
    f.write('\n'.join(good_pairs))
    f.close()


    adjs_reg = lex.loc[(lex.cgram == 'ADJ')&(lex.cgramortho == 'ADJ')&(lex.genre == 'f') & (lex.nblettres >= 5)&(lex.nombre == 's')]
    adjs_reg_m = adjs_reg.lemme.to_list()
    adjs_reg_f = adjs_reg.ortho.to_list()
    pairs_adjs = []
    for i in range(len(adjs_reg)):
        if adjs_reg_m[i]!=adjs_reg_f[i]:
            line = adjs_reg_m[i]+"\t"+adjs_reg_f[i]
            pairs_adjs.append(line)
    f = open("paires-adjs.txt", "w")
    f.write('\n'.join(pairs_adjs))
    f.close()


if __name__ == '__main__':
    main()
