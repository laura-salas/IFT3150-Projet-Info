import os
import pandas

import assign_infos
import cleaning_pairs
import lemmatizer
import clean_data
import embeddings_analysis
import plot_results

def main():
	'''
	# 1. assign_infos :
	if not os.path.isdir("\REPERE\CLEANED\words_assigned.txt"):
		assign_infos.main()

	# 2. clean data
	if len(os.listdir('/home/varun/temp') ) == 0:
		clean_data.main()

	lemmatize.main()
	'''
	scores_results = embeddings_analysis.main()
	print("scores_results:",scores_results)
	pure_scores_results = scores_results[0]
	plot_results.extract_pairs_scores(pure_scores_results, "pure_score")

	lem_scores_results = scores_results[1]
	plot_results.extract_pairs_scores(lem_scores_results, "lemma_score")

	stem_scores_results = scores_results[2]
	plot_results.extract_pairs_scores(stem_scores_results, "stem_score")

if __name__ == '__main__':
    main()
