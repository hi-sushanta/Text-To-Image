import torch
import torchvision
from torchvision import transforms
from transformers import T5Tokenizer
from torch import nn
import numpy as np
import matplotlib.pyplot as plt

from torch.utils.data import Dataset,DataLoader
from PIL import Image

class CustomDataset(Dataset):
    
    def __init__(self,base_dir,image_with_text,target_imgsize=(256,256)):
        self.image_with_text = image_with_text
        self.base_dir = base_dir
        self.target_imgsize = target_imgsize
        self.tokenizer = T5Tokenizer.from_pretrained("t5-large")
        self.tokenizer.require_grad = False
        self.transform = transforms.Compose([
        transforms.ToTensor(), # Scales data into [0,1]
        transforms.Resize(target_imgsize),
        transforms.Lambda(lambda t: (t * 2) - 1) # Scale between [-1, 1]
        ])
    def __len__(self):
        return len(self.image_with_text)

    def __getitem__(self,idx):

        image_path = self.base_dir + self.image_with_text[idx][0]
        src_text = self.image_with_text[idx][1]

        image = Image.open(image_path).convert("RGB")
        image = self.transform(image)
        
        token = self.tokenizer(src_text,return_tensors="pt",max_length=512,padding='max_length').input_ids
        token = torch.from_numpy(np.array(token))

        return image,token,src_text