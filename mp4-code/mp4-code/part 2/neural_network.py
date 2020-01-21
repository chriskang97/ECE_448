import numpy as np # <- Nice :)

"""
    Minigratch Gradient Descent Function to train model
    1. Format the data
    2. call four_nn function to obtain losses
    3. Return all the weights/biases and a list of losses at each epoch
    Args:
        epoch (int) - number of iterations to run through neural net
        w1, w2, w3, w4, b1, b2, b3, b4 (numpy arrays) - starting weights
        x_train (np array) - (n,d) numpy array where d=number of features
        y_train (np array) - (n,) all the labels corresponding to x_train
        num_classes (int) - number of classes (range of y_train)
        shuffle (bool) - shuffle data at each epoch if True. Turn this off for testing.
    Returns:
        w1, w2, w3, w4, b1, b2, b3, b4 (numpy arrays) - resulting weights
        losses (list of ints) - each index should correspond to epoch number
            Note that len(losses) == epoch
    Hints:
        Should work for any number of features and classes
        Good idea to print the epoch number at each iteration for sanity checks!
        (Stdout print will not affect autograder as long as runtime is within limits)
"""
def minibatch_gd(epoch, w1, w2, w3, w4, b1, b2, b3, b4, x_train, y_train, num_classes, shuffle=True):

    #IMPLEMENT HERE

    num_image = x_train.shape[0]
    # Current Idea : Shuffle the Indices and retrieve a new batch of training per epoch
    n_indices = np.arange(num_image )
    total_loss = []
    leftover = 0 ;

    # print(w1.shape)
    # print(w2.shape)
    # print(w3.shape)
    # print(w4.shape)

    #print(n_indices)
    for ep in range (epoch) :
        losses = []

        #Step #1 : Shuffle the Training Data if true
        if ( shuffle ) :
            np.random.shuffle(n_indices)

        #Step #2 : Split the Training Data to 200 Batch Size
        num_batch = np.floor( num_image / 200 )

        leftover_image = num_image % 200

        if (leftover_image != 0) :
            num_batch += 1
            leftover = 1 ;

        #Step #3 : RAM IT THROUGH THE NETWORK!!!!!!!!!!!!!!!!!!
        for batch in range( int(num_batch) ) :

            if ( num_batch - 1 == batch and leftover ) :
                split_batch_indices = n_indices[batch*200 : (batch)*200 + leftover_image ]
            else :
                split_batch_indices = n_indices[batch*200 : (batch+1)*200 ]

            split_batch = x_train[split_batch_indices]
            split_batch_label = y_train[split_batch_indices]
            w1, w2, w3, w4, b1, b2, b3, b4, loss_epoch = four_nn( w1, w2, w3, w4, b1, b2, b3, b4, split_batch, split_batch_label)

            losses.append(loss_epoch)

        total_loss.append( np.sum(losses) )

        print("Epoch ", ep , ": ", total_loss[ep] )


    return w1, w2, w3, w4, b1, b2, b3, b4, total_loss

"""
    Use the trained weights & biases to see how well the nn performs
        on the test data
    Args:
        All the weights/biases from minibatch_gd()
        x_test (np array) - (n', d) numpy array
        y_test (np array) - (n',) all the labels corresponding to x_test
        num_classes (int) - number of classes (range of y_test)
    Returns:
        avg_class_rate (float) - average classification rate
        class_rate_per_class (list of floats) - Classification Rate per class
            (index corresponding to class number)
    Hints:
        Good place to show your confusion matrix as well.
        The confusion matrix won't be autograded but necessary in report.
"""
def test_nn(w1, w2, w3, w4, b1, b2, b3, b4, x_test, y_test, num_classes):
    classes = np.bincount(y_test)

    avg_class_rate = 0.0
    class_rate_per_class = [0.0] * num_classes

    Z1, cache_1 = affine_forward(x_test, w1, b1)
    A1, Z1 = relu_forward(Z1)

    Z2, cache_2 = affine_forward(A1, w2, b2)
    A2, Z2 = relu_forward(Z2)

    Z3, cache_3 = affine_forward(A2, w3, b3 )
    A3, Z3 = relu_forward(Z3)

    Z4, cache_4 = affine_forward(A3, w4, b4 )

    loss, dF = cross_entropy(Z4, y_test )
    ##print(loss)

    identify_class = np.argmax(Z4, axis = 1 )
    print(identify_class)

    num_class = np.bincount(identify_class)
    avg_class_rate = np.sum(1*(identify_class == y_test))/ len(y_test)

    for i in range(num_classes):
        if i == 0:
            truth = -num_classes*(y_test == i)

            alt_identify_class = identify_class - num_classes
            class_rate_per_class[i] = np.sum(1*(alt_identify_class == truth ) ) / classes[i]
        else:
            truth = (i+1)*(y_test == i) - 1

            class_rate_per_class[i] = np.sum(1*(identify_class == truth ) ) / classes[i]


    #for i in range(len(y_test)):
        #if



    ##print(Z4[0])


    return avg_class_rate, class_rate_per_class

"""
    4 Layer Neural Network
    Helper function for minibatch_gd
    Up to you on how to implement this, won't be unit tested
    Should call helper functions below
"""
def four_nn(w1, w2, w3, w4, b1, b2, b3, b4, input, input_label):

    Z1, cache_1 = affine_forward(input, w1, b1)
    A1, Z1 = relu_forward(Z1)

    Z2, cache_2 = affine_forward(A1, w2, b2)
    A2, Z2 = relu_forward(Z2)

    Z3, cache_3 = affine_forward(A2, w3, b3 )
    A3, Z3 = relu_forward(Z3)

    Z4, cache_4 = affine_forward(A3, w4, b4 )


    # print(input.shape)
    # print(Z1.shape)
    # print(Z2.shape)
    # print(Z3.shape)
    # print(Z4.shape)


    loss, dF = cross_entropy(Z4, input_label )

    #BACKWARD PROPOGATIONNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
    dA3, dW4, dB4 = affine_backward(dF, cache_4 )
    # print(dA3.shape)
    # print(dW4.shape)
    dZ3 = relu_backward(dA3, Z3 )
    dA2, dW3, dB3 = affine_backward( dZ3, cache_3 )

    dZ2 = relu_backward(dA2, Z2 )
    dA1, dW2, dB2 = affine_backward( dZ2, cache_2 )

    dZ1 = relu_backward(dA1, Z1 )
    dA0, dW1, dB1 = affine_backward( dZ1, cache_1 )


    # UPDATING WEIGHTTTTTTS AND BIASSSSSSSSS
    # print(dA3.shape)
    # print(dF.shape)
    # print(dW4.shape)

    lp = 0.1

    w4 = w4 - lp*dW4
    b4 = b4 - lp*dB4

    w3 = w3 - lp*dW3
    b3 = b3 - lp*dB3

    w2 = w2 - lp*dW2
    b2 = b2 - lp*dB2

    w1 = w1 - lp*dW1
    b1 = b1 - lp*dB1

    pass

    return w1, w2, w3, w4, b1, b2, b3, b4, loss



"""
    Next five functions will be used in four_nn() as helper functions.
    All these functions will be autograded, and a unit test script is provided as unit_test.py.
    The cache object format is up to you, we will only autograde the computed matrices.

    Args and Return values are specified in the MP docs
    Hint: Utilize numpy as much as possible for max efficiency.
        This is a great time to review on your linear algebra as well.
"""
def affine_forward(A, W, b):
    #Z = np.sum( np.dot(A,W), axis = 0 ) + b

    Z = np.dot(A,W)  + b
    cache = (A, W, b)

    # cache["A"] = A
    # cache["W"] = W

    return Z, cache

def affine_backward(dZ, cache):
    # dA = np.sum(np.dot(dZ, cache["W"]), axis=1 )
    # dW = np.sum( np.dot(cache["A"], dZ), axis=0)
    # dB = np.sum(dZ, axis=1)

    dA = np.dot(dZ, cache[1].T )
    dW = np.dot(cache[0].T, dZ )
    dB = np.sum(dZ, axis=0)

    #dW = np.reshape(dW, (-1,1) )
    return dA, dW, dB

def relu_forward(Z):
    A = np.zeros( (Z.shape[0], Z.shape[1] ) )
    A = np.maximum(Z,A)

    cache = Z

    return A, cache

def relu_backward(dA, cache):

    first_term = 1 * ( cache > 0 )
    dZ = first_term * dA

    return dZ

def cross_entropy(F, y):
    n = len(y)

    tuple_input = ( np.arange(n), np.int8(y) )
    first_term = F[tuple_input]
    second_term = np.sum( np.exp(F), axis = 1 )

    loss = (-1/n) * np.sum( first_term - np.log(second_term ) )

    # Backward Propagation

    first_term = np.zeros( (F.shape[0], F.shape[1]) )
    first_term[tuple_input] = 1

    #first_term = 1 * (classified_class == y )
    #first_term = np.array(first_term)

    denominator = second_term
    denominator = np.reshape(denominator, (-1,1) )
    numerator = np.exp(F)

    #first_term = np.reshape(first_term, (-1, 1) )

    dF = (-1/n) * ( first_term - (numerator/denominator )  )

    return loss, dF
