## TODO: define the convolutional neural network architecture

import torch
import torch.nn as nn
import torch.nn.functional as F
# can use the below import should you choose to initialize the weights of your Net
import torch.nn.init as I


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        
        ## TODO: Define all the layers of this CNN, the only requirements are:
        ## 1. This network takes in a square (same width and height), grayscale image as input
        ## 2. It ends with a linear layer that represents the keypoints
        ## it's suggested that you make this last layer output 136 values, 2 for each of the 68 keypoint (x, y) pairs
        
        # As an example, you've been given a convolutional layer, which you may (but don't have to) change:
        # 1 input image channel (grayscale), 32 output channels/feature maps, 5x5 square convolution kernel
        # input 1,225,225 //(225-5)/1 +1 = 221 // output 32,221,221
        # output after maxpool: 32,110,110
        self.conv1 = nn.Conv2d(1, 32, 3) 
        self.conv1_bn2 = nn.BatchNorm2d(32)
        # output after maxpool: 64,54,54
        self.conv2 = nn.Conv2d(32, 64, 3)
        self.conv2_bn2 = nn.BatchNorm2d(64)
        # output after maxpool: 128,26,26
        self.conv3 = nn.Conv2d(64, 128, 3)
        self.conv3_bn2 = nn.BatchNorm2d(128)
        # output after maxpool: 256,12,12
        self.conv4 = nn.Conv2d(128, 256, 3)
        self.conv4_bn2 = nn.BatchNorm2d(256)
        # Maxpooling layer
        self.pool = nn.MaxPool2d(2, 2)
        
        # Fully connected layers
        self.fc1 = nn.Linear(12*12*256, 3000)
        self.fc1_bn1 = nn.BatchNorm1d(3000)
        self.fc2 = nn.Linear(3000, 1000)
        self.fc2_bn1 = nn.BatchNorm1d(1000)
        self.fc3 = nn.Linear(1000,136)
        
        self.dropout = nn.Dropout(0.15)


        ## Note that among the layers to add, consider including:
        # maxpooling layers, multiple conv layers, fully-connected layers, and other layers (such as dropout or batch normalization) to avoid overfitting
        

        
    def forward(self, x):
        ## TODO: Define the feedforward behavior of this model
        ## x is the input image and, as an example, here you may choose to include a pool/conv step:
        x = self.dropout(self.pool(F.relu(self.conv1_bn2(self.conv1(x)))))
        x = self.dropout(self.pool(F.relu(self.conv2_bn2(self.conv2(x)))))
        x = self.dropout(self.pool(F.relu(self.conv3_bn2(self.conv3(x)))))
        x = self.dropout(self.pool(F.relu(self.conv4_bn2(self.conv4(x)))))
        # Flatten layer
        x = x.view(x.size(0), -1)
        x = self.dropout(F.relu(self.fc1_bn1(self.fc1(x))))
        x = self.dropout(F.relu(self.fc2_bn1(self.fc2(x))))
        x = self.fc3(x) 
        # a modified x, having gone through all the layers of your model, should be returned
        return x
