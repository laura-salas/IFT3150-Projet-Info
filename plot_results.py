import matplotlib.pyplot as plt

'''
On regarde la performance si on prend les top-k paires de plus haut score,
    ou k varie de 1 à 350.
Pour chaque valeur de k,
on peut calculer si une paire dans les top-k est biaisée (precision)
et on peut aussi calculer le % des paires biaisées qui se trouvent dans le top k. (rappel).
'''


def extract_pairs_scores(results, score_type):
    """
    Sort all 350 pairs by the current score type (ascending)
    :param results: our dataset
    :param score_type: the score type for this
    :return:
    """
    sorted_results = results[['paire (m)', 'paire (f)', score_type, 'bias (m)', 'bias (f)']].\
		sort_values(by=[score_type])
    precisions = []
    recalls = []

    for k in range(len(sorted_results)):
        precisions.append(performance_top_k(sorted_results, k)[0])
        recalls.append(performance_top_k(sorted_results, k)[1])
    generate_plot(range(len(sorted_results)), precisions,
				  recalls, len(sorted_results), score_type)


def performance_top_k(results, k):
    """
    Allows us to assess performance in our dataset given a slice of size k
    These are sorted in descending order.

    :param results: our entire output
    :param k: how many k-elements to evaluate
    :return: precision and recall calculated for our k values
    """
    k_results = results.iloc[:k]
    true_positive = 0
    false_positive = 0
    for i in range(k):
        # Assumer que tout le top-k est biaisé
        if k_results.iloc[i]['bias (m)'] == 1 or k_results.iloc[i]['bias (f)'] == 1:
            # la paire etait biaisée et on a déterminé qu'elle l'était
            true_positive += 1
        else:
            # la paire etait non biaisée et on a déterminé qu'elle l'était
            false_positive += 1

    # la paire etait biaisée et on a déterminé qu'elle ne l'était pas
    false_negative = len(k_results) - k

    if true_positive != 0:
        precision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + false_negative)
    else:
        precision, recall = 0, 0

    return precision, recall


def generate_plot(k, precision, recall, size_of_data, score_type):
    """
    Generate plot for our data type, one data point at a time.
    :param k: current k-slice
    :param precision: current precision value
    :param recall:  current recall value
    :param size_of_data: total size of our data
    :param score_type: which score we are dealing with (pure, lemmatized, stemmed.

    """
    plt.plot(k, precision, label="Performance du modèle", color="red")
    plt.plot(k, recall, label="Rappel du modèle", color="blue")
    plt.legend()
    plt.xlabel("Top-k")
    plt.ylabel("Performance")
    plt.title("Qualité de score: " + score_type)
    plt.grid(True)
    plt.xlim([1, size_of_data])
    # uncomment the following to show the interactive graph
    # plt.show()
    plt.savefig('graphique-%s.jpg' % score_type)
    # comment the following to "stack" the curves
    plt.clf()

