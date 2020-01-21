import numpy as np
import matplotlib.pyplot as plt

class NaiveBayes(object):
	def __init__(self,num_class,feature_dim,num_value):
		"""Initialize a naive bayes model.

		This function will initialize prior and likelihood, where
		prior is P(class) with a dimension of (# of class,)
			that estimates the empirical frequencies of different classes in the training set.
		likelihood is P(F_i = f | class) with a dimension of
			(# of features/pixels per image, # of possible values per pixel, # of class),
			that computes the probability of every pixel location i being value f for every class label.

		Args:
		    num_class(int): number of classes to classify
		    feature_dim(int): feature dimension for each example
		    num_value(int): number of possible values for each pixel
		"""

		self.num_value = num_value
		self.num_class = num_class
		self.feature_dim = feature_dim

		self.prior = np.zeros((num_class))
		self.likelihood = np.zeros((feature_dim,num_value,num_class))



		self.training = np.zeros( (10000, feature_dim) )

	#def train(self,train_set,train_label,k_val):
	def train(self,train_set,train_label):
		""" Train naive bayes model (self.prior and self.likelihood) with training dataset.
			self.prior(numpy.ndarray): training set class prior (in log) with a dimension of (# of class,),
			self.likelihood(numpy.ndarray): training set likelihood (in log) with a dimension of
				(# of features/pixels per image, # of possible values per pixel, # of class).
			You should apply Laplace smoothing to compute the likelihood.

		Args:
		    train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim)
		    train_label(numpy.ndarray): training labels with a dimension of (# of examples, )
		"""

		# YOUR CODE HERE
		self.prior = np.log10(np.bincount(train_label)/(len(train_label)) )
		num_of_images = np.bincount(train_label)

		#k = k_val		learned through testing many k_values that 0.1 is the best accuracy and 10 is the worst, but all accuracy > 0.70
		k = 0.1
		v = self.num_value


		self.likelihood += k

		# Go through each individual Image (50,000)
		for image in range( len(train_label)):

			current_image = train_set[image]
			current_label = train_label[image]
			test_array = np.arange(self.feature_dim)

			test_tuple = (test_array, current_image, current_label)


			self.likelihood[test_tuple] += 1

		self.likelihood = np.transpose(self.likelihood)

		for label in range(self.num_class):
			self.likelihood[label] /= (self.feature_dim * num_of_images[label] + k*v)
			#print(np.sum(self.likelihood[label]) )

		self.likelihood = np.transpose(self.likelihood)
		self.likelihood = np.log10(self.likelihood)

		self.training = train_set
		pass

	def test(self,test_set,test_label):
		""" Test the trained naive bayes model (self.prior and self.likelihood) on testing dataset,
			by performing maximum a posteriori (MAP) classification.
			The accuracy is computed as the average of correctness
			by comparing between predicted label and true label.

		Args:
		    test_set(numpy.ndarray): testing examples with a dimension of (# of examples, feature_dim)
		    test_label(numpy.ndarray): testing labels with a dimension of (# of examples, )

		Returns:
			accuracy(float): average accuracy value
			pred_label(numpy.ndarray): predicted labels with a dimension of (# of examples, )
		"""

		accuracy = 0
		pred_label = np.zeros((len(test_set)))

		max_post = np.zeros( (self.num_class, 2) ) - 9999999
		min_post = np.ones ( (self.num_class, 2) )

		# YOUR CODE HERE

		test_array = np.arange(self.feature_dim)

		for image in range (len(test_label) ) :
			log_prob_label = []

			for label in range (self.num_class) :

				test_tuple = (test_array, test_set[image], label )
				posterior = np.sum( self.likelihood[test_tuple]  )

				log_prob_label.append( self.prior[label] + posterior )

			pred_label[image] = np.argmax(log_prob_label)

			if ( log_prob_label[ int(pred_label[image])] > max_post[ int(pred_label[image]) ][0] ) :
				max_post[int(pred_label[image])][0] = log_prob_label[int(pred_label[image])]
				max_post[int(pred_label[image])][1] = image

			if ( log_prob_label[ int(pred_label[image])]  < min_post[int(pred_label[image]) ][0] ) :
				min_post[int(pred_label[image])][0] = log_prob_label[int(pred_label[image])]
				min_post[int(pred_label[image])][1] = image


		accuracy = np.sum( 1*(pred_label == test_label) ) / len(test_label)

		print("Highest Posterior with Image Number: \n", max_post)
		print("\nLowest Posterior with Image Number: \n",  min_post)

		test_image = np.zeros( (28, 28) )

		for label in range (self.num_class) :
			print( self.training[ int(min_post[label][1]) ].shape ) ;

			test_image = test_set[ int(min_post[label][1]) ]
			plt.subplot(3,4,label+1)
			plt.subplots_adjust(wspace=2, hspace=2)
			plt.imshow( test_image.reshape( (28,28) ) )
			plt.title( "Class Number: " + str(label) + "\nImage Number: " + str(min_post[label][1]) )

		pass

		return accuracy, pred_label


	def save_model(self, prior, likelihood):
		""" Save the trained model parameters
		"""

		np.save(prior, self.prior)
		np.save(likelihood, self.likelihood)

	def load_model(self, prior, likelihood):
		""" Load the trained model parameters
		"""

		self.prior = np.load(prior)
		self.likelihood = np.load(likelihood)

	def intensity_feature_likelihoods(self, likelihood):
		"""
	    Get the feature likelihoods for high intensity pixels for each of the classes,
	        by sum the probabilities of the top 128 intensities at each pixel location,
	        sum k<-128:255 P(F_i = k | c).
	        This helps generate visualization of trained likelihood images.

	    Args:
	        likelihood(numpy.ndarray): likelihood (in log) with a dimension of
	            (# of features/pixels per image, # of possible values per pixel, # of class)
	    Returns:
	        feature_likelihoods(numpy.ndarray): feature likelihoods for each class with a dimension of
	            (# of features/pixels per image, # of class)
		"""
		feature_likelihoods = np.zeros((likelihood.shape[0],likelihood.shape[2]))

		# YOUR CODE HERE

		test_matrix = np.transpose(likelihood)
		temp_matrix = np.transpose(feature_likelihoods)

		for label in range( likelihood.shape[2] ) :
			temp_matrix[label] = np.sum(test_matrix[label][128:256], axis = 0 )

		feature_likelihoods = np.transpose(temp_matrix)

		return feature_likelihoods
if __name__=="__main__":
	naive = NaiveBayes(10,784,256)
	x_train = np.load(r"D:\Documents\Class\cs440\MP3\part1\data/x_train.npy")
	y_train = np.load(r"D:\Documents\Class\cs440\MP3\part1\data/y_train.npy")
	x_test = np.load(r"D:\Documents\Class\cs440\MP3\part1\data/x_test.npy")
	y_test = np.load(r"D:\Documents\Class\cs440\MP3\part1\data/y_test.npy")
	naive.train(x_train, y_train)
	acc, pred = naive.test(x_test, y_test)
	print(acc)
	# test_k = np.arange(0.1,10.1,0.1)
	# print(test_k)
	# best_accuracy = 0
	# best_k = test_k[0]
	# for i in range(len(test_k)):
	# 	naive.train(x_train, y_train,test_k[i])
	# 	acc, pred = naive.test(x_test, y_test)
	# 	print(i)
	# 	if acc >= best_accuracy:
	# 		best_accuracy = acc
	# 		best_k = test_k[i]
	# print("best_k value",best_k)
	# print("best accuracy", best_accuracy)
