# https://github.com/pytorch/vision/blob/master/torchvision/transforms.py

import torch
from torchvision import transforms
import random

input_size = 224 # currenttly fixed
train_scale = 256 # currently not used in 'train'
test_scale = 256
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

def my_transform(img):
    img = transforms.resize(img, test_scale)
    imgs = transforms.ten_crop(img, input_size)  # this is a list of PIL Images
    return torch.stack([normalize(transforms.to_tensor(x)) for x in imgs], 0) # returns a 4D tensor

# following ResNet paper, note that here do not use crop
def my_transform_multiscale_test(img): 
    # add flips ?
    test_scales = [224, 256, 384, 480, 640]
    imgs = [transforms.resize(img, scale) for scale in test_scales]
    return torch.stack([normalize(transforms.to_tensor(x)) for x in imgs], 0) 

composed_data_transforms = {
    'train': transforms.Compose([
        transforms.RandomSizedCrop(input_size), 
        transforms.RandomHorizontalFlip(), 
        transforms.ToTensor(), 
        normalize
    ]),
    'multi_scale_train': transforms.Compose([   ## following ResNet paper, but not include the standard color augmentation from AlexNet
        transforms.Resize(random.randint(256, 480)),  # May be adjusted to be bigger
        transforms.RandomCrop(input_size),  # not RandomSizedCrop
        transforms.RandomHorizontalFlip(), 
        transforms.ColorJitter(), # different from AlexNet's PCA method which is adopted in the ResNet paper?
        transforms.ToTensor(), 
        normalize
    ]),
    'validation': transforms.Compose([
        transforms.Resize(test_scale),  
        transforms.CenterCrop(input_size),
        transforms.ToTensor(),
        normalize
    ]),
    'test': transforms.Compose([
        transforms.Resize(test_scale),  
        transforms.CenterCrop(input_size),
        transforms.ToTensor(),
        normalize
    ]),
    'ten_crop': my_transform
    ,
    'multi_scale_test': my_transform_multiscale_test
}


def data_transforms(phase):
    return composed_data_transforms[phase]