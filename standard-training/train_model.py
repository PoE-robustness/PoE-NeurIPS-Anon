import os 
import argparse 


parser = argparse.ArgumentParser(description='Wrapper for easy evaluation of downloaded models.')
parser.add_argument('--folder', default='cifar10_LeNet5-relu_0.1', type=str)
args = parser.parse_args()

LR = float(args.folder.rsplit('_')[-1])
print(LR)
if 'cifar10_LeNet5-relu' in args.folder:
    cmd = 'python cifar_plus.py -a LeNet5-relu --train-batch 64 --test-batch 256 --wd 0 --momentum 0 --lr {} --checkpoint train_checkpoints/cifar10_LeNet5-relu_{} --epochs 25'.format(LR, LR)
elif 'cifar10_LeNet5-tanh' in args.folder:
    cmd = 'python cifar_plus.py -a LeNet5-tanh --train-batch 64 --test-batch 256 --wd 0 --momentum 0 --lr {} --checkpoint train_checkpoints/cifar10_LeNet5-tanh_{} --epochs 18'.format(LR, LR)
elif 'cifar10_resnet20' in args.folder:
    cmd = 'python cifar_plus.py -a resnet --lr {} --depth 20 --epochs 164 --schedule 81 122 --gamma 0.1 --wd 1e-4 --checkpoint train_checkpoints/cifar10_resnet20_{}'.format(LR, LR)
elif 'cifar10_resnet50' in args.folder:
    cmd = 'python cifar_plus.py -a resnet --lr {} --depth 50 --epochs 164 --schedule 81 122 --gamma 0.1 --wd 1e-4 --checkpoint train_checkpoints/cifar10_resnet50_{}'.format(LR, LR)
elif 'cifar10_resnet110' in args.folder:
    cmd = 'python cifar_plus.py -a resnet --lr {} --depth 110 --epochs 164 --schedule 81 122 --gamma 0.1 --wd 1e-4 --checkpoint train_checkpoints/cifar10_resnet110_{}'.format(LR, LR)
elif 'cifar10_densenet' in args.folder:
    cmd = 'python cifar_plus.py -a densenet --lr {} --depth 40 --growthRate 12 --train-batch 64 --epochs 300 --schedule 150 225 --wd 1e-4 --gamma 0.1 --checkpoint train_checkpoints/cifar10_densenet_{}'.format(LR, LR)
elif 'cifar100_resnet50' in args.folder:
    cmd = 'python cifar_plus.py -a resnet --dataset cifar100 --lr {} --depth 50 --epochs 164 --schedule 81 122 --gamma 0.1 --wd 1e-4 --checkpoint train_checkpoints/cifar100_resnet50_{}'.format(LR, LR)
elif 'cifar100_resnet110' in args.folder:
    cmd = 'python cifar_plus.py -a resnet --dataset cifar100 --lr {} --depth 110 --epochs 164 --schedule 81 122 --gamma 0.1 --wd 1e-4 --checkpoint train_checkpoints/cifar100_resnet110_{}'.format(LR, LR)
elif 'cifar100_densenet' in args.folder:
    cmd = 'python cifar_plus.py -a densenet --dataset cifar100 --lr {} --depth 40 --growthRate 12 --train-batch 64 --epochs 300 --schedule 150 225 --wd 1e-4 --gamma 0.1 --checkpoint train_checkpoints/cifar100_densenet_{}'.format(LR, LR)

os.system(cmd)