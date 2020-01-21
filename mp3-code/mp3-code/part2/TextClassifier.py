# TextClassifier.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Dhruv Agarwal (dhruva2@illinois.edu) on 02/21/2019
import math
"""
You should only modify code within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
class TextClassifier(object):
    def __init__(self):
        """Implementation of Naive Bayes for multiclass classification
        :param lambda_mixture - (Extra Credit) This param controls the proportion of contribution of Bigram
        and Unigram model in the mixture model. Hard Code the value you find to be most suitable for your model
        """
        #self.prior = 0
        self.prior = []
        self.posterior = []
        self.index = {}
        self.lambda_mixture = 0.5
        self.labels = 0

        # BIGRAM VARIABLE
        self.bigram_posterior = []
        self.bigram_index = {}

    def fit(self, train_set, train_label):
        """
        :param train_set - List of list of words corresponding with each text
            example: suppose I had two emails 'i like pie' and 'i like cake' in my training set
            Then train_set := [['i','like','pie'], ['i','like','cake']]

        :param train_labels - List of labels corresponding with train_set
            example: Suppose I had two texts, first one was class 0 and second one was class 1.
            Then train_labels := [0,1]
        """

        # TODO: Write your code here

        unique_word = []
        bag_of_word = {}
        words_in_doc = {}
        doc_per_label = {}

        for doc in range(len(train_set)) :          #for each document

            unique_word_in_doc = set(train_set[doc])    #get all the unique words
            label = train_label[doc]                    #get the label

            for word in unique_word_in_doc :            #iterate through each unique word
                new_tuple = (word, label)               #create tuple of unique word and label

                # Count Unique Word per Label
                if new_tuple not in bag_of_word :
                    bag_of_word[new_tuple] = 1
                    unique_word.append(word)
                else :
                    bag_of_word[new_tuple] += 1

            # Counter Number of Documnets Per Label
            if label not in doc_per_label :
                doc_per_label[label] = 1
            else :
                doc_per_label[label] += 1
        ##FIX THIS
        total = len(train_label)            #total number of docs
        #for i in range(1,max(train_label)+1):           #go through each class
        for i in range(1,15):
            if i not in doc_per_label:
                self.prior.append(0)
            else:
                prior = float(doc_per_label[i] / total)
                self.prior.append(prior)                    #append to list


        counter = 0

        unique_word = set(unique_word)
        for word in unique_word :
            self.index[word] = counter
            self.posterior.append([])

            for label in range (1, max(train_label) + 1 ) :
                new_tuple = (word, label)
                if new_tuple in bag_of_word :
                    posterior_value = (bag_of_word[new_tuple] + 1) / (doc_per_label[label] + 2)
                else :
                    posterior_value = (0.1 + 1) / (doc_per_label[label] + 2 + 0.1 * len(unique_word) )

                self.posterior[counter].append(posterior_value)

            counter += 1
        self.labels = max(train_label)

        print( len(unique_word))
        print( len(self.index.keys()) )
        #uniform prior
        uniform_prior = float ( len(unique_word)/max(train_label) )

        #print(self.posterior)

        # BIGRAM VARIABLES
        bigram_of_word = {}
        unique_bigram = []

        ## BIGRAM TEST
        for doc in range(len(train_set)) :          #for each document

            bigram_word = []
            total_word = len(train_set[doc])

            label = train_label[doc]                    #get the label
            word_set_1 = train_set[doc]
            word_set_2 = word_set_1[1:total_word]

            word_set_1.remove(word_set_1[-1] )

            for i in range(total_word - 1) :
                bigram_word.append( word_set_1[i] + word_set_2[i]  )

            unique_bigram_in_doc = set(bigram_word)


            for biword in unique_bigram_in_doc :            #iterate through each unique word
                new_tuple = (biword, label)               #create tuple of unique word and label

                # Count Unique Word per Label
                if new_tuple not in bigram_of_word :
                    bigram_of_word[new_tuple] = 1
                    unique_bigram.append(biword)
                else :
                    bigram_of_word[new_tuple] += 1


        counter = 0
        unique_bigram = set(unique_bigram)

        for bigram in unique_bigram :
            self.bigram_index[bigram] = counter
            self.bigram_posterior.append([])

            for label in range (1, max(train_label) + 1 ) :
                new_tuple = (bigram, label)
                if new_tuple in bigram_of_word :
                    posterior_value = (bigram_of_word[new_tuple] + 1) / (doc_per_label[label] + 2)
                else :
                    posterior_value = (0.1 + 1) / (doc_per_label[label] + 2 + 0.1 * len(unique_bigram) )

                self.bigram_posterior[counter].append(posterior_value)

            counter += 1

        pass

    def predict(self, x_set, dev_label,lambda_mix=0.0):
        """
        :param dev_set: List of list of words corresponding with each text in dev set that we are testing on
              It follows the same format as train_set
        :param dev_label : List of class labels corresponding to each text
        :param lambda_mix : Will be supplied the value you hard code for self.lambda_mixture if you attempt extra credit

        :return:
                accuracy(float): average accuracy value for dev dataset
                result (list) : predicted class for each text
        """

        accuracy = 0.0
        result = []

        # TODO: Write your code here
        correct = 0

        for doc in range(len(x_set)):
            unique_word_in_doc = set(x_set[doc])
            real_label = dev_label[doc]
            value = 0
            best_guess = 0
            best_value = 0

            for label in range(self.labels):
                alpha = 0
                #beta = math.log10(self.prior)          #for uniform prior
                if self.prior[label] == 0:
                    continue
                else:
                    beta = math.log10(self.prior[label])
                for word in unique_word_in_doc:
                    if word in self.index:
                        index = self.index[word]
                        lamdah = self.posterior[index][label]
                        opp_lamdah = 1 - lamdah
                        alpha += math.log10(lamdah/opp_lamdah)
                        beta += math.log10(opp_lamdah)

                value_1 = beta + alpha
                #print(value)



                # BIGRAM INCLUSION

                bigram_word = []
                total_word = len(x_set[doc])

                if ( total_word != 0 and total_word != 1 ) :

                    word_set_1 = x_set[doc]
                    word_set_2 = word_set_1[1:total_word]

                    word_set_1.remove(word_set_1[-1] )

                    for i in range(total_word - 1) :
                        bigram_word.append( word_set_1[i] + word_set_2[i]  )

                    unique_bigram_in_doc = set(bigram_word)

                    bi_alpha = 0
                    #beta = math.log10(self.prior)          #for uniform prior
                    if self.prior[label] == 0:
                        continue
                    else:
                        bi_beta = math.log10(self.prior[label])
                    for bigram in unique_bigram_in_doc:
                        if bigram in self.bigram_index:
                            index = self.bigram_index[bigram]
                            lamdah = self.bigram_posterior[index][label]
                            opp_lamdah = 1 - lamdah
                            bi_alpha += math.log10(lamdah/opp_lamdah)
                            bi_beta += math.log10(opp_lamdah)

                    value_2 = bi_beta + bi_alpha
                else :
                    value_2 = 0

                true_value = value_1 * (1-self.lambda_mixture) + value_2 * self.lambda_mixture

                # Make the Prediction here
                if true_value > best_value or best_value == 0 :
                    best_guess = label + 1
                    best_value = true_value

            result.append(best_guess)

            if best_guess == dev_label[doc]:
                correct += 1
        accuracy = float(correct / len(dev_label))
        # print (result)
        # print (dev_label)
        pass

        return accuracy,result
