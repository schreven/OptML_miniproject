# -*- coding: utf-8 -*-
"""
Created on Wed May 23 18:16:08 2018

@authors: Musluoglu Cem Ates, Novakovic Milica, van Schreven Cyril
"""
import torch
import math
import os

from torch import optim
from torch import Tensor
from torch.autograd import Variable
from torch import nn
from sklearn.model_selection import KFold
from torch.utils.data.sampler import SubsetRandomSampler
import matplotlib.pyplot as plt
import numpy as np

from visualizing import plot_acc_loss
from models import create_1layer_model, create_convex_model, get_datasets
from training_and_validating import train_validate_kfold, train_test
from sweeps import grid_search_lr, grid_search_beta
import argparse


### UNCOMMENT RELEVANT BLOCKS FOR REPRODUCTION, RUN load_arrs_save_figs.py

if __name__ == '__main__':
    all_code_pieces = '[all, sgd_one_layer, grid_search_betas_adam_one_layer, lr_search_adam_one_layer, lr_search_amsgrad_one_layer,\
    adam_one_layer, amsgrad_one_layer, sgd_testing_one_layer, adam_testing_one_layer, amsgrad_testing_one_layer, \
    sgd_convex, lr_search_adam_convex, lr_search_amsgrad_convex, adam_convex, amsgrad_convex, \
    sgd_testing_convex, adam_testing_convex, amsgrad_testing_convex]'
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--code_name', default = 'sgd_one_layer', type=str, help='Name of the piece of code to run'+all_code_pieces+'.')
    args = parser.parse_args()
    code_name = args.code_name
    ######### ONE HIDDEN LAYER MODEL ###############

    if code_name not in all_code_pieces:
        print("[ERROR] code_name not valid.")
    else:
        print("Running code correponding to: "+str(code_name)+'.')
    ### SIMPLE SGD ONE_LAYER
    if code_name == 'sgd_one_layer' or code_name == 'all':
        model = create_1layer_model
        kfold = 5
        nb_epochs = 40
        lr = 1e-1
        mini_batch = 100
        train_dataset, train_loader, test_dataset, test_loader = get_datasets(mini_batch_size = mini_batch)
        interstates = True

        optimizer_ = optim.SGD
        opt_parameters_SGD = [lr]

        train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold = train_validate_kfold(\
                model, optimizer_, opt_parameters_SGD, train_dataset, kfold=kfold, shuffle=True, nb_epochs = nb_epochs, mini_batch_size = mini_batch, interstates = interstates)

        plot_acc_loss(train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold)

        save_array = [train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold]
        np.save(os.path.join('../array_and_figures','1st_kf=5_epo=40_lr=1e-1_btch=100_SGD_inter'),save_array)


    ### GRID SEARCH BETAS ADAM ONE_LAYER
    if code_name == 'grid_search_betas_adam_one_layer' or code_name == 'all':
        #grid_search_beta()
        res = np.load(os.path.join('../array_and_figures','grid_kf=5_epo=40_lr=1e-3_btch=100_Adam_beta1_beta2.npy'))
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

        sns.heatmap(val_acc, xticklabels=np.reshape(np.array(beta2_list),(-1,1)), yticklabels=np.reshape(np.array(beta1_list),(-1,1))).set_title('Validating accuracy mean')
        plt.figure()


    ### LR SEARCH ADAM ONE_LAYER
    if code_name == 'lr_search_adam_one_layer' or code_name == 'all':
        grid_search_lr()
        res = np.load(os.path.join('../array_and_figures','grid_kf=4_epo=120_b1=0.91_b2=0.999_btch=100_Adam_lr.npy'))
        res = dict(res.tolist())
        lr_list = [0.00001, 0.0001, 0.001, 0.01, 0.1]
        num_lr = len(lr_list)
        val_acc = np.mean(res['val_acc'], axis=1)
        plt.figure()
        plt.semilogx(lr_list, val_acc)
        plt.title('Validating accuracy mean')



    ### LR SEARCH AMSGRAD ONE_LAYER

    if code_name == 'lr_search_amsgrad_one_layer' or code_name == 'all':
        res = np.load(os.path.join('../array_and_figures','grid_kf=5_epo=40_b1=0.91_b2=0.999_btch=100_AmsGrad_lr.npy'))
        res = dict(res.tolist())
        lr_list = [0.00001, 0.0001, 0.001, 0.01, 0.1]
        num_lr = len(lr_list)
        val_acc = np.mean(res['val_acc'], axis=1)
        plt.figure()
        plt.semilogx(lr_list, val_acc)
        plt.title('Validating accuracy mean')


    ### SIMPLE ADAM ONE_LAYER
    if code_name == 'adam_one_layer' or code_name == 'all':
        model = create_1layer_model
        kfold = 4
        nb_epochs = 40
        lr = 1e-3
        beta1, beta2 = 0.91, 0.999
        amsgrad = False
        mini_batch = 100
        train_dataset, train_loader, test_dataset, test_loader = get_datasets(mini_batch_size = mini_batch)
        interstates = True

        optimizer_ = optim.Adam
        opt_parameters_Adam = [lr, (beta1, beta2), amsgrad]

        train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold = train_validate_kfold(\
                model, optimizer_, opt_parameters_Adam, train_dataset, kfold=kfold, shuffle=True, nb_epochs = nb_epochs, mini_batch_size = mini_batch, interstates = interstates)

        plot_acc_loss(train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold)

        save_array = [train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold]
        np.save(os.path.join('../array_and_figures','2nd_kf=4_epo=40_lr=1e-3_btch=100_Adam_inter'),save_array)



    ### Improved ADAM: AMSGRAD ONE_LAYER
    if code_name == 'amsgrad_one_layer' or code_name == 'all':
        model = create_1layer_model
        kfold = 4
        nb_epochs = 40
        lr = 1e-3
        beta1, beta2 = 0.91, 0.999
        amsgrad = True
        mini_batch = 100
        train_dataset, train_loader, test_dataset, test_loader = get_datasets(mini_batch_size = mini_batch)
        interstates = True

        optimizer_ = optim.Adam
        opt_parameters_Adam = [lr, (beta1, beta2), amsgrad]

        train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold = train_validate_kfold(\
                model, optimizer_, opt_parameters_Adam, train_dataset, kfold=kfold, shuffle=True, nb_epochs = nb_epochs, mini_batch_size = mini_batch, interstates = interstates)

        plot_acc_loss(train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold)

        save_array = [train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold]
        np.save(os.path.join('../array_and_figures','3rd_kf=4_epo=40_lr=1e-3_btch=100_AMSGRAD_inter'),save_array)




    ### SGD TESTING ONE_LAYER
    if code_name == 'sgd_testing_one_layer' or code_name == 'all':
        model = create_1layer_model
        nb_epochs = 40
        lr = 1e-1
        mini_batch = 100
        train_dataset, train_loader, test_dataset, test_loader = get_datasets(mini_batch_size = mini_batch)
        interstates = False

        optimizer_ = optim.SGD
        opt_parameters_SGD = [lr]


        train_loss, test_loss, train_acc, test_acc = train_test(\
                model, optimizer_, opt_parameters_SGD, train_dataset, test_dataset, shuffle=True, nb_epochs = nb_epochs, mini_batch_size = mini_batch, interstates = interstates)


        #plot_acc_loss(train_loss, test_loss, train_acc, test_acc)
        print('SGD test accuracy: {}'.format(test_acc))

        save_array = [train_loss, test_loss, train_acc, test_acc]
        np.save(os.path.join('../array_and_figures','4th_epo=40_lr=1e-1_btch=100_SGD_inter_testing'),save_array)

    ### ADAM TESTING ONE_LAYER
    if code_name == 'adam_testing_one_layer' or code_name == 'all':
        model = create_1layer_model
        nb_epochs = 40
        lr = 1e-3
        mini_batch = 100
        train_dataset, train_loader, test_dataset, test_loader = get_datasets(mini_batch_size = mini_batch)
        interstates = False


        beta1, beta2 = 0.91, 0.999
        amsgrad = False
        optimizer_ = optim.Adam
        opt_parameters_Adam = [lr, (beta1, beta2), amsgrad]

        train_loss, test_loss, train_acc, test_acc = train_test(\
                model, optimizer_, opt_parameters_Adam, train_dataset, test_dataset, shuffle=True, nb_epochs = nb_epochs, mini_batch_size = mini_batch, interstates = interstates)


        #plot_acc_loss(train_loss, test_loss, train_acc, test_acc)
        print('ADAM test accuracy: {}'.format(test_acc))

        save_array = [train_loss, test_loss, train_acc, test_acc]
        np.save(os.path.join('../array_and_figures','5th_epo=40_lr=1e-3_btch=100_Adam_inter_testing'),save_array)

    ### AMSGRAD TESTING ONE_LAYER

    if code_name == 'amsgrad_testing_one_layer' or code_name == 'all':
        model = create_1layer_model
        nb_epochs = 40
        lr = 1e-3
        mini_batch = 100
        train_dataset, train_loader, test_dataset, test_loader = get_datasets(mini_batch_size = mini_batch)
        interstates = False


        beta1, beta2 = 0.91, 0.999
        amsgrad = True
        optimizer_ = optim.Adam
        opt_parameters_Adam = [lr, (beta1, beta2), amsgrad]

        train_loss, test_loss, train_acc, test_acc = train_test(\
                model, optimizer_, opt_parameters_Adam, train_dataset, test_dataset, shuffle=True, nb_epochs = nb_epochs, mini_batch_size = mini_batch, interstates = interstates)


        #plot_acc_loss(train_loss, test_loss, train_acc, test_acc)
        print('ADAM test accuracy: {}'.format(test_acc))

        save_array = [train_loss, test_loss, train_acc, test_acc]
        np.save(os.path.join('../array_and_figures','6th_epo=40_lr=1e-3_btch=100_AMSGRAD_inter_testing'),save_array)

    ########### CONVEX MODEL ################

    ### SIMPLE SGD CONVEX
    if code_name == 'sgd_convex' or code_name == 'all':
        model = create_convex_model
        kfold = 5
        nb_epochs = 40
        lr = 1e-1
        mini_batch = 100
        train_dataset, train_loader, test_dataset, test_loader = get_datasets(mini_batch_size = mini_batch)
        interstates = True
        run_once = True

        optimizer_ = optim.SGD
        opt_parameters_SGD = [lr]

        train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold = train_validate_kfold(\
                model, optimizer_, opt_parameters_SGD, train_dataset, kfold=kfold, shuffle=True, nb_epochs = nb_epochs, mini_batch_size = mini_batch, interstates = interstates, run_once = run_once)

        plot_acc_loss(train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold)

        save_array = [train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold]
        np.save(os.path.join('../array_and_figures','1st_kf=5_epo=40_lr=1e-1_btch=100_SGD_inter_ro_convex'),save_array)



    ### LR SEARCH ADAM CONVEX

    if code_name == 'lr_search_adam_convex' or code_name == 'all':
        model = create_convex_model

        #grid_search_lr(model)
        res = np.load(os.path.join('../array_and_figures','grid_kf=5_epo=120_b1=0.91_b2=0.999_btch=100_Adam_lr_ro_convex.npy'))
        res = dict(res.tolist())
        lr_list = [0.00001, 0.0001, 0.001, 0.01, 0.1]
        num_lr = len(lr_list)
        val_acc = res['val_acc']
        plt.figure()
        plt.semilogx(lr_list, val_acc)
        plt.title('Validating accuracy mean')

    ### LR SEARCH AMSGRAD CONVEX

    if code_name == 'lr_search_amsgrad_convex' or code_name == 'all':
        #model = create_convex_model
        #grid_search_lr(model)
        res = np.load(os.path.join('../array_and_figures','grid_kf=5_epo=40_b1=0.91_b2=0.999_btch=100_AmsGrad_lr_ro_CONV.npy'))
        res = dict(res.tolist())
        lr_list = [0.00001, 0.0001, 0.001, 0.01, 0.1]
        num_lr = len(lr_list)
        val_acc = np.mean(res['val_acc'], axis=1)
        plt.figure()
        plt.semilogx(lr_list, val_acc)
        plt.title('Validating accuracy mean')

    ### SIMPLE ADAM CONVEX
    if code_name == 'adam_convex' or code_name == 'all':

        model = create_convex_model
        kfold = 4
        nb_epochs = 40
        lr = 1e-4
        beta1, beta2 = 0.90, 0.999
        amsgrad = False
        mini_batch = 100
        train_dataset, train_loader, test_dataset, test_loader = get_datasets(mini_batch_size = mini_batch)
        interstates = True
        run_once = True

        optimizer_ = optim.Adam
        opt_parameters_Adam = [lr, (beta1, beta2), amsgrad]

        train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold = train_validate_kfold(\
                model, optimizer_, opt_parameters_Adam, train_dataset, kfold=kfold, shuffle=True, nb_epochs = nb_epochs, mini_batch_size = mini_batch, interstates = interstates, run_once = run_once)

        plot_acc_loss(train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold)

        save_array = [train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold]
        np.save(os.path.join('../array_and_figures','2nd_kf=4_epo=40_lr=1e-3_btch=100_Adam_inter_ro_CONV_'),save_array)

    ### Improved ADAM: AMSGRAD CONVEX
    if code_name == 'amsgrad_convex' or code_name == 'all':

        model = create_convex_model
        kfold = 4
        nb_epochs = 40
        lr = 1e-3
        beta1, beta2 = 0.90, 0.999
        amsgrad = True
        mini_batch = 100
        train_dataset, train_loader, test_dataset, test_loader = get_datasets(mini_batch_size = mini_batch)
        interstates = True
        run_once = True

        optimizer_ = optim.Adam
        opt_parameters_Adam = [lr, (beta1, beta2), amsgrad]

        train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold = train_validate_kfold(\
                model, optimizer_, opt_parameters_Adam, train_dataset, kfold=kfold, shuffle=True, nb_epochs = nb_epochs, mini_batch_size = mini_batch, interstates = interstates, run_once = run_once)

        plot_acc_loss(train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold)

        save_array = [train_loss_kfold, val_loss_kfold, train_acc_kfold, val_acc_kfold]
        np.save(os.path.join('../array_and_figures','3rd_kf=4_epo=40_lr=1e-3_btch=100_AMSGRAD_inter_ro_CONV_'),save_array)

    ### SGD TESTING CONVEX
    if code_name == 'sgd_testing_convex' or code_name == 'all':
        model = create_convex_model
        nb_epochs = 40
        lr = 1e-1
        mini_batch = 100
        train_dataset, train_loader, test_dataset, test_loader = get_datasets(mini_batch_size = mini_batch)
        interstates = False

        optimizer_ = optim.SGD
        opt_parameters_SGD = [lr]


        train_loss, test_loss, train_acc, test_acc = train_test(\
                model, optimizer_, opt_parameters_SGD, train_dataset, test_dataset, shuffle=True, nb_epochs = nb_epochs, mini_batch_size = mini_batch, interstates = interstates)


        #plot_acc_loss(train_loss, test_loss, train_acc, test_acc)
        print('SGD test accuracy: {}'.format(test_acc))

        save_array = [train_loss, test_loss, train_acc, test_acc]
        np.save(os.path.join('../array_and_figures','4th_epo=40_lr=1e-1_btch=100_SGD_inter_convex_testing'),save_array)

    ### ADAM TESTING CONVEX
    if code_name == 'adam_testing_convex' or code_name == 'all':
        model = create_convex_model
        nb_epochs = 40
        lr = 1e-4
        mini_batch = 100
        train_dataset, train_loader, test_dataset, test_loader = get_datasets(mini_batch_size = mini_batch)
        interstates = False


        beta1, beta2 = 0.91, 0.999
        amsgrad = False
        optimizer_ = optim.Adam
        opt_parameters_Adam = [lr, (beta1, beta2), amsgrad]

        train_loss, test_loss, train_acc, test_acc = train_test(\
                model, optimizer_, opt_parameters_Adam, train_dataset, test_dataset, shuffle=True, nb_epochs = nb_epochs, mini_batch_size = mini_batch, interstates = interstates)


        #plot_acc_loss(train_loss, test_loss, train_acc, test_acc)
        print('ADAM test accuracy: {}'.format(test_acc))

        save_array = [train_loss, test_loss, train_acc, test_acc]
        np.save(os.path.join('../array_and_figures','5th_epo=40_lr=1e-3_btch=100_Adam_inter_testing_convex'),save_array)

    ### AMSGRAD TESTING CONVEX
    if code_name == 'amsgrad_testing_convex' or code_name == 'all':

        model = create_convex_model
        nb_epochs = 40
        lr = 1e-3
        mini_batch = 100
        train_dataset, train_loader, test_dataset, test_loader = get_datasets(mini_batch_size = mini_batch)
        interstates = False


        beta1, beta2 = 0.91, 0.999
        amsgrad = True
        optimizer_ = optim.Adam
        opt_parameters_Adam = [lr, (beta1, beta2), amsgrad]

        train_loss, test_loss, train_acc, test_acc = train_test(\
                model, optimizer_, opt_parameters_Adam, train_dataset, test_dataset, shuffle=True, nb_epochs = nb_epochs, mini_batch_size = mini_batch, interstates = interstates)


        #plot_acc_loss(train_loss, test_loss, train_acc, test_acc)
        print('ADAM test accuracy: {}'.format(test_acc))

        save_array = [train_loss, test_loss, train_acc, test_acc]
        np.save(os.path.join('../array_and_figures','6th_epo=40_lr=1e-3_btch=100_AMSGRAD_inter_testing_convex'),save_array)
