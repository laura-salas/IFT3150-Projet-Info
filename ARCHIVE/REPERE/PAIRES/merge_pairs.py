src_path_b = "Repertoire de paires\paires-langlais.txt"
src_path_a = "Repertoire de paires\paires-Lareau.txt"
a = open(src_path_a, "r", encoding="utf-8").read()
b = open(src_path_b, "r", encoding="utf-8").read()

b_clean_one = b.split(" \n")
c = []
d = a.split("\n")
a_clean = []
for line in d:
    line.replace("\t", "")
    a_clean.append(line.split("	"))

b_clean = []
for lined in b_clean_one:
    b_clean.append(lined.split(" (")[0].split(" "))


final = a_clean
ad = 0

for line in b_clean:
    if line not in final and (line.copy()).reverse() not in final:
        final.append(line)

final.remove([''])
final_dict = {}
for line in final:
    if len(line) == 2:
        if line[0] not in final_dict:
            final_dict[line[0]] = {}
            final_dict[line[0]]["fem"] = line[1]

final = []
for masc in final_dict.keys():
    final.append(masc + " " + final_dict[masc]["fem"])
    # print(masc, final_dict[masc]["fem"])

final = list(dict.fromkeys(final))
final = sorted(final)
for line in final:
    print(line)