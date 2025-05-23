import torch
print(torch.__version__)  # Версия PyTorch
print(torch.version.cuda)  # Версия CUDA, под которую собран PyTorch
print(torch.cuda.is_available())