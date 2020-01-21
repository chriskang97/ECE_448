import numpy as np

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

		k = 1
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

		self.likelihood = np.transpose(self.likelihood)
		self.likelihood = np.log10(self.likelihood)

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

		# YOUR CODE HERE

		test_array = np.arange(self.feature_dim)

		for image in range (len(test_label) ) :
			log_prob_label = []

			for label in range (self.num_class) :

				test_tuple = (test_array, test_set[image], label )
				posterior = np.sum( self.likelihood[test_tuple]  )

				log_prob_label.append( self.prior[label] + posterior )

			pred_label[image] = np.argmax(log_prob_label)


		accuracy = np.sum( 1*(pred_label == test_label) ) / len(test_label)

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

		print(test_matrix[0][128:256].shape )

		for label in range( likelihood.shape[2] ) :
			temp_matrix[label] = np.sum(test_matrix[label][128:256], axis = 0 )

		feature_likelihoods = np.transpose(temp_matrix)

		return feature_likelihoods

if __name__=="__main__":
	naive = NaiveBayes(10,784,256)
	x_train = np.load(r"C:/Users/chris/Downloads/ECE_448/mp3-code/mp3-code/part1/data/x_train.npy")
	y_train = np.load(r"C:/Users/chris/Downloads/ECE_448/mp3-code/mp3-code/part1/data/y_train.npy")

	x_test = np.load(r"C:/Users/chris/Downloads/ECE_448/mp3-code/mp3-code/part1/data/x_test.npy")
	y_test = np.load(r"C:/Users/chris/Downloads/ECE_448/mp3-code/mp3-code/part1/data/y_test.npy")
	#print(x_train[0])
	#print(y_train[0])
	naive.train(x_train, y_train)
	accuracy, predicted_label = naive.test(x_test, y_test)
	feature_likelihoods = naive.intensity_feature_likelihoods(naive.likelihood )
	print("Accuracy: ", accuracy )
	print("\nPredicted Label: ", predicted_label )
	# print(naive.prior)
	# print(naive.likelihood)
