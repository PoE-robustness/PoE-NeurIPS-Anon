import os
import argparse
import torch
import torch.nn as nn
import torchvision.datasets as datasets
import torch.utils.data as data
import torchvision.transforms as transforms
from robustness.model_utils import make_and_restore_model
from robustness.datasets import DATASETS

import sys

# TODO: custom model import here
import torch.backends.cudnn as cudnn

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='./data')
    parser.add_argument('--norm', type=str, default='Linf')
    parser.add_argument('--epsilon', type=float, default=8./255.)
    parser.add_argument('--model_path', help='Model for attack evaluation')
    parser.add_argument('--model', '-m', default='resnet50', type=str, help='Name of the model')
    parser.add_argument('--n_ex', type=int, default=10000)
    parser.add_argument('--individual', action='store_true', default=False)
    #parser.add_argument('--save_dir', type=str, default='./results')
    parser.add_argument('--batch_size', type=int, default=500)
    parser.add_argument('--log_file', type=str, default='./log_file.txt')
    parser.add_argument('--version', type=str, default='standard')
    parser.add_argument('--random_seed', type=int, default=0)
    
    args = parser.parse_args()

    # torch seed
    torch.manual_seed(args.random_seed)

    # TODO: custom model load here
    dataset = DATASETS['cifar']('./data')
    model, _ = make_and_restore_model(arch=args.model, dataset=dataset, parallel = True, resume_path = args.model_path, add_custom_forward = True)
    
    # TODO: set model to eval mode
    model.eval()

    # TODO: custom logit retriever
    def get_only_logits(X):
        output = model(X)
        model_logits = output[0] if (type(output) is tuple) else output
        return model_logits

    # load data
    transform_list = [
        transforms.Resize(32),
        transforms.CenterCrop(32),
        transforms.ToTensor()
    ]
    transform_chain = transforms.Compose(transform_list)
    item = datasets.CIFAR10(root=args.data_dir, train=False, transform=transform_chain, download=True)
    test_loader = data.DataLoader(item, batch_size=1000, shuffle=False, num_workers=0)
    
    # # create save dir
    # if not os.path.exists(args.save_dir):
    #     os.makedirs(args.save_dir)
    
    # load attack    
    from autoattack import AutoAttack
    adversary = AutoAttack(get_only_logits, norm=args.norm, eps=args.epsilon, log_path=args.log_file,
        version=args.version)
    adversary.seed = args.random_seed # adversary seed
    
    l = [x for (x, y) in test_loader]
    x_test = torch.cat(l, 0)
    l = [y for (x, y) in test_loader]
    y_test = torch.cat(l, 0)
    
    # example of custom version
    if args.version == 'custom':
        adversary.attacks_to_run = ['apgd-ce', 'fab']
        adversary.apgd.n_restarts = 2
        adversary.fab.n_restarts = 2
    
    # run attack and save images
    with torch.no_grad():
        if not args.individual:
            adv_complete = adversary.run_standard_evaluation(x_test[:args.n_ex], y_test[:args.n_ex],
                bs=args.batch_size)
            
            # torch.save({'adv_complete': adv_complete}, '{}/{}_{}_1_{}_eps_{:.5f}.pth'.format(
            #     args.save_dir, 'aa', args.version, adv_complete.shape[0], args.epsilon))

        else:
            # individual version, each attack is run on all test points
            adv_complete = adversary.run_standard_evaluation_individual(x_test[:args.n_ex],
                y_test[:args.n_ex], bs=args.batch_size)
            
            # torch.save(adv_complete, '{}/{}_{}_individual_1_{}_eps_{:.5f}_plus_{}_cheap_{}.pth'.format(
            #     args.save_dir, 'aa', args.version, args.n_ex, args.epsilon))