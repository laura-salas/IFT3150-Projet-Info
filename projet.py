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
	results = embeddings_analysis.main()
	plot_results.extract_pairs_scores(results, score_type)

if __name__ == '__main__':
    main()
