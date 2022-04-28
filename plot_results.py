import os
import assign_infos
import cleaning_pairs
import lemmatizer
import clean_data
import pandas


'''
On regarde la performance si on prend les top-k paires de plus haut score,
	ou k varie de 1 à 350.
Pour chaque valeur de k,
on peut calculer si une paire dans les top-k est biaisée (precision)
et on peut aussi calculer le % des paires biaisées qui se trouvent dans le top k. (rappel).
'''
def extract_pairs_scores(results, score_type):
	# Trier les 350 paires par un score
	res = results[['paire_m','paire_f',score_type,'bias']].sort_values(by=[score_type])
	#res_pairs = (res['paire_m'], res['paire_f'])
	#res_scores = res[score_type]
	precisions = []
	recalls = []
	# Regarder la performance si on prend les top-k paires de plus haut score
	# donc du plus biaisé au moins biaisé
	# (en prenant pour acquis que notre mesure fonctionne bien)
	for k in range(len(res)):
		precisions.append(perfo_top_k(res,k)[0])
		recalls.append(perfo_top_k(res,k)[1])
	generate_plot(range(len(res)),precisions, recalls)

def perfo_top_k(res,k):
	res = res().iloc[:k]
	'''
	# Pour chaque valeur de k, on calcule rappel et precision

	perfo = 0
	for i in range(k):
		# on assume que tout le top-k est biaisé

		if res['bias']==1:
			# la paire etait biaisée et on a déterminé qu'elle l'était
			# true positive
			tp += 1
		else:
			# la paire etait non biaisée et on a déterminé qu'elle l'était
			# false positive
			fp += 1
	# la paire etait biaisée et on a déterminé qu'elle ne l'était pas
	# false negative
	fn = len(res) - k

	precision = tp/(tp+fp)
	recall = tp/(tp+fn)
	'''

	return precision, recall



# Affichage des graphiques
def generate_plot(k,precision,recall):
	plt.plot(k, precision, label="Performance du modèle", color="red")
	plt.plot(k, recall, label="Rappel du modèle", color="blue")
	plt.xlabel("Top-k")
	plt.ylabel("Performance")
	plt.title("Qualité de score: "+score_type)
	plt.grid(True)
	plt.show()


def main():
	extract_pairs_scores(results, "lemma_score")


if __name__ == '__main__':
	main()
