#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 21:25:32 2017

@author: wayne

- torch resnet 152, Preact ResNet 50
    ResNet152-places365 trained from scratch using Torch: torch model converted caffemodel:deploy weights. It is the original ResNet with 152 layers. On the validation set, the top1 error is 45.26% and the top5 error is 15.02%.
    ResNet50-places365 trained from scratch using Torch: torch model. It is Preact ResNet with 50 layers. The top1 error is 44.82% and the top5 error is 14.71%.
    https://github.com/clcarwin/convert_torch_to_pytorch
        import vgg16
        model = vgg16.vgg16
        model.load_state_dict(torch.load('vgg16.pth'))
        model.eval()

    处理sequential: https://discuss.pytorch.org/t/how-to-modify-the-final-fc-layer-based-on-the-torch-model/766/11
"""

#pkill -9 python
#nvidia-smi
import os
import torch
import torch.nn as nn
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
import torchvision
from torchvision import transforms
import json
#plt.ion()   # interactive mode
#%matplotlib inline

with open('/home/wayne/python/kaggle/Ai_challenger/classification/ai_challenger_scene_train_20170904/scene_train_annotations_20170904.json', 'r') as f: #label文件
    label_raw_train = json.load(f)
with open('/home/wayne/python/kaggle/Ai_challenger/classification/ai_challenger_scene_validation_20170908/scene_validation_annotations_20170908.json', 'r') as f: #label文件
    label_raw_val = json.load(f)

label_raw_train[0]['label_id']
len(label_raw_train)

class SceneDataset(Dataset):

    def __init__(self, json_labels, root_dir, transform=None):
        """
        Args:
            json_labesl (list):read from official json file.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.label_raw = json_labels
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.label_raw)

    def __getitem__(self, idx):
        img_name = os.path.join(self.root_dir, self.label_raw[idx]['image_id'])
        image = Image.open(img_name)
        label = int(self.label_raw[idx]['label_id'])

        if self.transform:
            image = self.transform(image)

        return image, label

data_transforms = {
    'train': transforms.Compose([
        transforms.RandomSizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Scale(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}
transformed_dataset_train = SceneDataset(json_labels=label_raw_train,
                                    root_dir='/home/wayne/python/kaggle/Ai_challenger/classification/ai_challenger_scene_train_20170904/scene_train_images_20170904',
                                           transform=data_transforms['train']
                                           )      
transformed_dataset_val = SceneDataset(json_labels=label_raw_val,
                                    root_dir='/home/wayne/python/kaggle/Ai_challenger/classification/ai_challenger_scene_validation_20170908/scene_validation_images_20170908',
                                           transform=data_transforms['val']
                                           )         
batch_size = 2
dataloader = {'train':DataLoader(transformed_dataset_train, batch_size=batch_size,shuffle=True, num_workers=8),
             'val':DataLoader(transformed_dataset_val, batch_size=batch_size,shuffle=True, num_workers=8)
             }
dataset_sizes = {'train': len(label_raw_train), 'val':len(label_raw_val)}
use_gpu = torch.cuda.is_available()
#use_gpu = False

def imshow(inp, title=None):
    """Imshow for Tensor."""
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = std * inp + mean
    plt.imshow(inp)
    if title is not None:
        plt.title(title)
    plt.pause(1)  # pause a bit so that plots are updated


# Get a batch of training data
inputs, classes = next(iter(dataloader['train']))

# Make a grid from batch
out = torchvision.utils.make_grid(inputs)

imshow(out)


'''
new code from here: use .pth converted from .t7
'''

#from functools import partial
#import pickle
#
#arch = 'resnet152_places365'  
#model_weight = '%s.pth' % arch
#
#pickle.load = partial(pickle.load, encoding="latin1")
#pickle.Unpickler = partial(pickle.Unpickler, encoding="latin1")
##model = torch.load(model_file, map_location=lambda storage, loc: storage, pickle_module=pickle)
#
#if use_gpu == 1:
#    model_conv = torch.load(model_weight, pickle_module=pickle)
#else:
#    model_conv = torch.load(model_weight, map_location=lambda storage, loc: storage, pickle_module=pickle) # model trained in GPU could be deployed in CPU machine like this!
#
import resnet152_places365

model = resnet152_places365.resnet152_places365
model.load_state_dict(torch.load('resnet152_places365.pth'))
#model.eval()

print(model)

#model_conv = torchvision.models.resnet18(pretrained=True)
#for param in model_conv.parameters():
#    param.requires_grad = False

# Parameters of newly constructed modules have requires_grad=True by default
#num_ftrs = model_conv.fc.in_features
#model_conv.fc = nn.Linear(num_ftrs, 80)

model._modules['10']._modules['1'] = nn.Linear(2048, 8)  #依据上面打印出的model编号信息！！！
print(model)


import Preact_resnet50_places365

model2 = Preact_resnet50_places365.Preact_resnet50_places365
model2.load_state_dict(torch.load('Preact_resnet50_places365.pth'))
print(model2)
#print(model2._modules['12'])
model2._modules['12']._modules['1'] = nn.Linear(2048, 8)  #依据上面打印出的model编号信息！！！
print(model2)
