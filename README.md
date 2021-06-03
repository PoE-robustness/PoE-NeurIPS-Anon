# 1. Setup
## 1.1 Anaconda virtual environment

Create a conda environment named DL_env with all dependencies, run below
```
conda env create -f environment.yml
```

*Please note that we used a server with 2 Nvidia GPUs (each with 24 GB memory) for our code below.*

# 2. Evaluating saved models
## 2.1 standard-training
### 2.1.1 First, download a model checkpoint from below into standard-training/checkpoints/
https://drive.google.com/drive/folders/1vLtC62dTxFi1_uia8bx0chX5AK1ztOiK?usp=sharing

### 2.1.2 Then run the corresponding commands below:
```
cd standard-training
python eval_model.py --file checkpoints/${File Name} --gpu-id ${N}
```
#### where ${File Name} for each result in Table 1 (of paper) can be found below and ${N} is the gpu id (e.g. 0 or 1 or 2).

|  Dataset |      Model     | lr (base) | lr (2/L) | lr (1/L) | ${File Name}              |
|:--------:|:--------------:|:---------:|:--------:|:--------:|---------------------------|
|  CIFAR10 | LeNet 5 (relu) |    0.1    |   0.04   |   0.02   | cifar10_LeNet5-relu_${lr} |
|          | LeNet 5 (tanh) |    0.1    |   0.125  |  0.0625  | cifar10_LeNet5-tanh_${lr} |
|          |    ResNet 20   |    0.1    |  0.5672  |  0.2836  | cifar10_resnet20_${lr}    |
|          |    ResNet 50   |    0.1    |  0.1852  |  0.0926  | cifar10_resnet50_${lr}    |
|          |   ResNet 110   |    0.1    |  0.1709  |  0.0855  | cifar10_resnet110_${lr}   |
|          |   DenseNet 40  |    0.1    |  0.3683  |  0.1842  | cifar10_densenet_${lr}    |
| CIAFR100 |    ResNet 50   |    0.1    |  0.2286  |  0.1143  | cifar100_resnet50_${lr}   |
|          |   ResNet 110   |    0.1    |  0.1381  |  0.069   | cifar100_resnet110_${lr}  |
|          |   DenseNet 40  |    0.1    |   0.274  |   0.137  | cifar100_densenet_${lr}   |

#### Here is an example,
```
python eval_model.py --file checkpoints/cifar10_LeNet5-relu_0.1 --gpu-id 0
```
* First, eval_model.py will generate 10000 adversarial images and save in PGD/cifar10_LeNet5-relu_0.1/ (ensure disk space!)
* Second, eval_model.py will evaluate on clean and adversarial images and print out accuracies
* Third, adversarial accuracies will also be saved to PGD/cifar10_LeNet5-relu_0.1/log.txt


## 2.2 adversarial-training
### 2.2.1 First, download a model checkpoint from below into the corresponding folder PGD-AT/ (OR) TRADES/ (OR) RST/ (OR) Wide-RST
https://drive.google.com/drive/folders/1vLtC62dTxFi1_uia8bx0chX5AK1ztOiK?usp=sharing

### 2.2.2 Then run the corresponding command below:
```
cd adversarial-training/${Approach}
python autoattack_evaluation.py --model_path ${File Name} --log_file ${Approach}_${lr}.log
```
#### where ${Approach}, ${lr} and ${File Name} for each result in Table 2 (of paper) can be found below:

| ${Approach} | Model     | lr (base) | lr (2/L) | lr (1/L) | ${File Name}           |
|:-----------:|-----------|:---------:|:--------:|:--------:|------------------------|
|    PGD-AT   | ResNet-50 |    0.1    |  0.1922  |  0.0961  | PGD-AT_${lr}.pt.latest |
|    TRADES   | WRN-34-10 |    0.1    |  0.2668  |  0.1334  | TRADES_${lr}.pt        |
|     RST     | WRN-28-10 |    0.1    |  0.1485  |  0.0743  | RST_${lr}.pt           |
|   Wide-RST  | WRN-34-15 |    0.1    |  0.1485  |  0.0743  | Wide-RST_${lr}.pt      |

#### Here is an example,
```
cd adversarial-training/PGD-AT
python autoattack_evaluation.py --model_path RST_0.1485.pt --log_file RST_0.1485.log
```

##### Note on epsilon for TRADES
Please add ``` --epsilon 0.031 ``` when running autoattack_evaluation.py for TRADES (for correct comparison with SOTA on Autoattack benchmark). Here is an example,
```
cd adversarial-training/TRADES
python autoattack_evaluation.py --epsilon 0.031 --model_path TRADES_0.2668.pt --log_file TRADES_0.2668.log
```

# 3. Training from scratch

## 3.1 standard-training
```
cd standard-training
python train_model.py --folder ${Folder Name}
```
where ${Folder Name} for each result can be found in the below table 

|  Dataset |      Model     | lr (base) | lr (2/L) | lr (1/L) | ${Folder Name}            |
|:--------:|:--------------:|:---------:|:--------:|:--------:|---------------------------|
|  CIFAR10 | LeNet 5 (relu) |    0.1    |   0.04   |   0.02   | cifar10_LeNet5-relu_${lr} |
|          | LeNet 5 (tanh) |    0.1    |   0.125  |  0.0625  | cifar10_LeNet5-tanh_${lr} |
|          |    ResNet 20   |    0.1    |  0.5672  |  0.2836  | cifar10_resnet20_${lr}    |
|          |    ResNet 50   |    0.1    |  0.1852  |  0.0926  | cifar10_resnet50_${lr}    |
|          |   ResNet 110   |    0.1    |  0.1709  |  0.0855  | cifar10_resnet110_${lr}   |
|          |   DenseNet 40  |    0.1    |  0.3683  |  0.1842  | cifar10_densenet_${lr}    |
| CIAFR100 |    ResNet 50   |    0.1    |  0.2286  |  0.1143  | cifar100_resnet50_${lr}   |
|          |   ResNet 110   |    0.1    |  0.1381  |  0.069   | cifar100_resnet110_${lr}  |
|          |   DenseNet 40  |    0.1    |   0.274  |   0.137  | cifar100_densenet_${lr}   |

* First, a model is trained and saved at ${Folder Name}/only_model.pth.tar. At the end, lipschitz constant will be estimated.
* Train / val performance is saved to a log file in the same folder.
* To evaluate the trained model, run below
```
python eval_model.py --file ${Folder Name}/checkpoint.pth.tar --gpu-id ${N} --trained-from-scratch
```

*Note on LeNet5 models in MNIST and CIFAR10:* Lipschitz constants not estimated because of low-epoch training limitations (see Appendix B in paper). Learning rates corresponding to 1/L and 2/L found by analysis (see Section 5.2 in paper) 

#### Here is an example,
```
python train_model.py --folder checkpoints/cifar10_resnet20_0.1
```

### 3.1.1 Notes
* In all cases above, the Ms and Ns used in estimation can be changed within utils/lipschitz.py > class Weibull_Fitter() > function fit()

## 3.2 adversarial-training
### 3.2.1 TRADES
```
cd adversarial-training/TRADES/
python train_trades_cifar10.py --lr ${lr} --model-dir TRADES_${\lr}
```
* Run above command for three ${lr} as given in the table in section 2.2.2 of this README.
* Running the above command will generate checkpoints every 25 epochs for 75 epochs. At the end, lipschitz constant will be estimated.
* To only estimate Lispchitz constant (after training), run
```
python train_trades_cifar10.py --model-dir TRADES_${\lr} --only-lipschitz
```
* To evaluate on autoattack, run
```
python autoattack_evaluation.py --epsilon 0.031 --model_path TRADES_${lr}/model-wideres-epoch75.pt --log_file TRADES_${lr}/auto.log
```

### 3.2.2 RST
#### 3.2.2.1 First download the unlabelled data used in RST from below into RST/data/ folder
[500K unlabeled data from TinyImages (with pseudo-labels)](https://drive.google.com/open?id=1LTw3Sb5QoiCCN-6Y5PEKkq9C9W60w-Hi)

#### 3.2.2.2 Then run the following commands
```
cd adversarial-training/RST/
python robust_self_training.py --lr ${lr} --aux_data_filename ti_500K_pseudo_labeled.pickle --model_dir RST_${lr}
```
* Run above command for three ${lr} as given in the table in section 2.2.2 of this README.
* Running the above command will generate checkpoints every 25 epochs for 200 epochs. At the end, lipschitz constant will be estimated.
* To only estimate Lispchitz constant (after training), run
```
python robust_self_training.py --lr ${lr} --model_dir RST_${lr} --only-lipschitz
```
* To evaluate on autoattack, run
```
python autoattack_evaluation.py --model_path RST_${lr}/checkpoint-epoch200.pt --log_file RST_${lr}/auto.log
```

### 3.2.3 Wide-RST
#### 3.2.3.1 First download the unlabelled data used in RST from below into Wide-RST/data/ folder
[500K unlabeled data from TinyImages (with pseudo-labels)](https://drive.google.com/open?id=1LTw3Sb5QoiCCN-6Y5PEKkq9C9W60w-Hi)

#### 3.2.3.2 Then run the following commands
```
cd adversarial-training/Wide-RST/
python robust_self_training.py --lr ${lr} --aux_data_filename ti_500K_pseudo_labeled.pickle --model_dir Wide-RST_${lr}
```
* Run above command for three ${lr} as given in the table in section 2.2.2 of this README.
* Running the above command will generate checkpoints every 25 epochs for 200 epochs. At the end, lipschitz constant will be estimated.
* To only estimate Lispchitz constant (after training), run
```
python robust_self_training.py --lr ${lr} --model_dir RST_${lr} --only-lipschitz
```
* To evaluate on autoattack, run
```
python autoattack_evaluation.py --model_path Wide-RST_${lr}/checkpoint-epoch200.pt --log_file Wide-RST_${lr}/auto.log
```


### 3.2.4 PGD-AT
```
cd adversarial-training/PGD-AT/
```
#### 3.2.4.1 SOTA PGD-AT, Lipschitz estimation
```
python robust_train.py --lr 0.1 --dataset cifar --data ./data --arch resnet50 --batch-size 256 --out-dir PGD-AT --exp-name SOTA_0.1 \
    --adv-train 1 --eps 8.0/255 --constraint inf --attack-steps 10 --attack-lr 0.007 --random-restarts 5
```
* Running the above command will generate a 'latest' checkpoint after 150 epochs. At the end, lipschitz constant will be estimated.

#### 3.2.4.2 Largest Convergent and Persistent PGD-AT
```
python robust_train_fast.py --lr ${lr} --dataset cifar --data ./data --arch resnet50 --batch-size 256 --out-dir PGD-AT --exp-name PE_${lr} \
    --adv-train 1 --eps 8.0/255 --constraint inf --attack-steps 10 --attack-lr 0.007 --random-restarts 5
```
* Run above command for *two* ${lr} (i.e. 2/L and 1/L) as given in the table in section 2.2.2 of this README.
* Running the above command will generate a 'latest' checkpoint after 150 epochs. Since, we are running robust_train_fast, this will not do lipschitz estimation again.
* To evaluate on autoattack, run
```
python autoattack_evaluation.py --model_path PGD-AT/PE_${lr}/checkpoint.pt.latest --log_file PGD-AT/PE_${lr}/auto.log
```

### 3.2.5 Notes
* In all 4 cases above, the Ms and Ns used in estimation can be changed within more_utils/lipschitz.py > class Weibull_Fitter() > function fit()


## 3.3 Figure 4 (CIFAR)
* Download figure_4_lipschitz.pth.tar from https://drive.google.com/drive/folders/1vLtC62dTxFi1_uia8bx0chX5AK1ztOiK?usp=sharing into standard-training/notebooks-figure-4/

Please note that our estimation procedure is inherently random and fixing seed will not solve this. To get the exact same plots in the appendix, we provide the saved gradients/weights in the file --> figure_4_lipschitz.pth.tar .

* Run notebook at standard-training/notebooks-figure-4/
* Intermediate cells will display both heat maps in Appendix B
* The last cell will display figure 4

## 3.4 Figure 3 (MNIST)
* Run notebooks at MNIST-figure-3/notebooks-figure-3/ 
* The second last cell will display the plot for the corresponding models
* The last cell will display the values in Table 1 (of paper) for MNIST which are obtained from the above plot


