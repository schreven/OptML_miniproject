# -*- coding: utf-8 -*-
"""
Created on Thu May 24 15:59:04 2018

@author: Bob
"""

import os
import pylab
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


### SGD

save_array = np.load(os.path.join('arrays_and_images','1st_kf=5_epo=40_lr=1e-1_btch=100_SGD_inter.npy'))


train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold = save_array


plt.figure()
title="MNIST loss"
sns.tsplot(np.array(train_loss_kfold)).set_title(title)
sns.tsplot(np.array(val_loss_kfold), color = 'r')
plt.legend(['Train', 'Validation'])
plt.xlabel('Epoch')
plt.ylabel('Loss')

pylab.savefig(os.path.join('arrays_and_images','first_vis.png'))



plt.figure()
title="MNIST accuracy"
sns.tsplot(np.array(train_acc_kfold)).set_title(title)
sns.tsplot(np.array(val_acc_kfold), color = 'r')
plt.legend(['Train', 'Validation'])
plt.xlabel('Epoch')
plt.ylabel('Accuracy')

pylab.savefig(os.path.join('arrays_and_images','second_vis.png'))




### SIMPLE ADAM

save_array = np.load(os.path.join('arrays_and_images','2nd_kf=4_epo=40_lr=1e-3_btch=100_Adam_inter.npy'))


train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold = save_array


plt.figure()
title="MNIST loss"
sns.tsplot(np.array(train_loss_kfold)).set_title(title)
sns.tsplot(np.array(val_loss_kfold), color = 'r')
plt.legend(['Train', 'Validation'])
plt.xlabel('Epoch')
plt.ylabel('Loss')

pylab.savefig(os.path.join('arrays_and_images','third_vis.png'))



plt.figure()
title="MNIST accuracy"
sns.tsplot(np.array(train_acc_kfold)).set_title(title)
sns.tsplot(np.array(val_acc_kfold), color = 'r')
plt.legend(['Train', 'Validation'])
plt.xlabel('Epoch')
plt.ylabel('Accuracy')

pylab.savefig(os.path.join('arrays_and_images','fourth_vis.png'))


### Updated ADAM: AMSGRAD

save_array = np.load(os.path.join('arrays_and_images','3rd_kf=4_epo=40_lr=1e-3_btch=100_AMSGRAD_inter.npy'))


train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold = save_array


plt.figure()
title="MNIST loss"
sns.tsplot(np.array(train_loss_kfold)).set_title(title)
sns.tsplot(np.array(val_loss_kfold), color = 'r')
plt.legend(['Train', 'Validation'])
plt.xlabel('Epoch')
plt.ylabel('Loss')

pylab.savefig(os.path.join('arrays_and_images','fifth_vis.png'))



plt.figure()
title="MNIST accuracy"
sns.tsplot(np.array(train_acc_kfold)).set_title(title)
sns.tsplot(np.array(val_acc_kfold), color = 'r')
plt.legend(['Train', 'Validation'])
plt.xlabel('Epoch')
plt.ylabel('Accuracy')

pylab.savefig(os.path.join('arrays_and_images','sixth_vis.png'))



### GRID
res = np.load(os.path.join('arrays_and_images','grid_kf=5_epo=40_lr=1e-3_btch=100_Adam_beta1_beta2.npy'))
res = dict(res.tolist())
beta1_list = [0.88, 0.89, 0.9, 0.91, 0.92]
beta2_list = [0.986, 0.99, 0.994, 0.998, 0.999, 0.9999]
num_b1 = len(beta1_list)
num_b2 = len(beta2_list)

val_acc = np.reshape(np.mean(res['val_acc'], axis=1),(num_b1,num_b2))
##correcting mistake in beta1_list
tmp = val_acc[2].copy()
val_acc[2] = val_acc[3]
val_acc[3] = tmp

plt.figure()
sns.heatmap(val_acc, xticklabels=np.reshape(np.array(beta2_list),(-1,1)), yticklabels=np.reshape(np.array(beta1_list),(-1,1))).set_title('Validating accuracy mean')

pylab.savefig(os.path.join('arrays_and_images','grid_vis.png'))




