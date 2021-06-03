import os 
import argparse 


parser = argparse.ArgumentParser(description='Wrapper for easy evaluation of downloaded models.')
parser.add_argument('--file', default='cifar10_LeNet5-relu_0.1', type=str)
parser.add_argument('--gpu-id', default=0, type=int)
parser.add_argument('--trained-from-scratch', action='store_true', default=False, help='set if you want to evaluate a model trained from scratch (instead of one downloaded)')
args = parser.parse_args()

LR_dotpth_dottar = args.file.rsplit('_')[-1]
LR = float(LR_dotpth_dottar[:-8]) # 0.123.pth.tar becomes 0.123
print(LR)
if 'cifar10_LeNet5-relu' in args.file:
    cmd = 'python cifar_adv.py -a LeNet5-relu --resume checkpoints/cifar10_LeNet5-relu_{}.pth.tar --adv_folder PGD/cifar10_LeNet5-relu_{} --gpu-id {}'.format(LR, LR, args.gpu_id)
elif 'cifar10_LeNet5-tanh' in args.file:
    cmd = 'python cifar_adv.py -a LeNet5-tanh --resume checkpoints/cifar10_LeNet5-tanh_{}.pth.tar --adv_folder PGD/cifar10_LeNet5-tanh_{} --gpu-id {}'.format(LR, LR, args.gpu_id)
elif 'cifar10_resnet20' in args.file:
    cmd = 'python cifar_adv.py -a resnet --depth 20 --resume checkpoints/cifar10_resnet20_{}.pth.tar --adv_folder PGD/cifar10_resnet20_{} --gpu-id {}'.format(LR, LR, args.gpu_id)
elif 'cifar10_resnet50' in args.file:
    cmd = 'python cifar_adv.py -a resnet --depth 50 --resume checkpoints/cifar10_resnet50_{}.pth.tar --adv_folder PGD/cifar10_resnet50_{} --gpu-id {}'.format(LR, LR, args.gpu_id)
elif 'cifar10_resnet110' in args.file:
    cmd = 'python cifar_adv.py -a resnet --depth 110 --resume checkpoints/cifar10_resnet110_{}.pth.tar --adv_folder PGD/cifar10_resnet110_{} --gpu-id {}'.format(LR, LR, args.gpu_id)
elif 'cifar10_densenet' in args.file:
    cmd = 'python cifar_adv.py -a densenet --depth 40 --growthRate 12 --resume checkpoints/cifar10_densenet_{}.pth.tar --adv_folder PGD/cifar10_densenet_{} --gpu-id {}'.format(LR, LR, args.gpu_id)
elif 'cifar100_resnet50' in args.file:
    cmd = 'python cifar_adv.py -a resnet --dataset cifar100 --depth 50 --resume checkpoints/cifar100_resnet50_{}.pth.tar --adv_folder PGD/cifar100_resnet50_{} --gpu-id {}'.format(LR, LR, args.gpu_id)
elif 'cifar100_resnet110' in args.file:
    cmd = 'python cifar_adv.py -a resnet --dataset cifar100 --depth 110 --resume checkpoints/cifar100_resnet110_{}.pth.tar --adv_folder PGD/cifar100_resnet110_{} --gpu-id {}'.format(LR, LR, args.gpu_id)
elif 'cifar100_densenet' in args.file:
    cmd = 'python cifar_adv.py -a densenet --dataset cifar100 --depth 40 --growthRate 12 --resume checkpoints/cifar100_densenet_{}.pth.tar --adv_folder PGD/cifar100_densenet_{} --gpu-id {}'.format(LR, LR, args.gpu_id)


if not args.trained_from_scratch:
    cmd = cmd + ' --downloaded_model'
os.system(cmd)