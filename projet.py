import embeddings_analysis
import plot_results


def main():
	scores_results = embeddings_analysis.main()
	plot_results.extract_pairs_scores(scores_results, "score_sim_pure")
	plot_results.extract_pairs_scores(scores_results, "score_sim_lemm")
	plot_results.extract_pairs_scores(scores_results, "score_sim_stemm")

if __name__ == '__main__':
    main()
