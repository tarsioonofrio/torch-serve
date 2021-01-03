import time

from PIL import Image
import torch
import torch.nn.functional as F
from torchvision import transforms
from torchvision import models

image_processing = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])


model = models.densenet161(pretrained=True)
model.eval()
model.cuda()

path_classification = '../serve/examples/image_classifier/kitten.jpg'

start_geral = time.time()
for i in range(10):
    start = time.time()

    im = Image.open(path_classification)
    tensor = image_processing(im)
    tensor = tensor.unsqueeze(0)
    tensor = tensor.cuda()
    output = model(tensor)
    out = F.softmax(output, dim=1)
    probs, classes = torch.topk(out, 1, dim=1)
    end = time.time()
    print(end - start)

end_geral = time.time()
print("Final time", end_geral - start_geral)
