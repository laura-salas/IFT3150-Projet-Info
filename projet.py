import os

import assign_infos
import cleaning_pairs
import lemmatizer
import clean_data

# PLAN
# 1. Establish, clean and verify names list :
# 		cleaning_pairs (not in this code ) then assign_infos
# 		mais cleaning_pairs
# 2. Access and clean corpus :
# 		clean_data.py
# 3. Lemmatize all the words except the ones listed (in step 1) :
# 		lemmatizer.py
#



def main():

	print("toast")

	# 1. assign_infos :
	if not os.path.isdir("\REPERE\CLEANED\words_assigned.txt"):
		assign_infos.main()

	# 2. clean data
	if len(os.listdir('/home/varun/temp') ) == 0:
		clean_data.main()

	lemmatize.main()



if __name__ == '__main__':
    main()
