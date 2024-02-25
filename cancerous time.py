# -*- coding = utf-8 -*-
# @Time : 2023/12/12 17:14
# @Author : Yourui Han
# @File : cancerous time.py
# @Software : PyCharm


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from som_position import train_SOM, feature_normalization, get_U_Matrix, get_winner_index, weights_PCA
import xlwt


def stage_normalization_weight_calculate(datas, labels):
    stage_weights = np.zeros(5)
    counts = np.zeros(5)
    for i in range(5):
        for j in range(len(labels)):
            if j == i:
                stage_weights[i] = stage_weights[i] + np.sum(datas[j])
                counts[i] = counts[i] + 1
    for i in range(5):
        stage_weights[i] = stage_weights[i] / counts[i]

    return stage_weights


def stage_normalization_entropy_calculate(datas, stage_weights, labels):
    # 计算每个病人的熵
    entropy_list = []
    for i in range(len(labels)):
        entropy = 0
        sum = np.sum(datas[i])
        for xi in datas[i]:
            if xi == 0:
                entropy = entropy + 0
            else:
                entropy = entropy + (sum / stage_weights[labels[i]]) * xi * np.log2(
                    (sum / stage_weights[labels[i]]) * xi)
        entropy_list.append(900 - entropy)
    return entropy_list



if __name__ == '__main__':
    data = pd.read_excel('TCGA_LUAD_all_deg_sur_expr.xlsx')
    labs = data['stage'].values
    label_names = {0: 'Normal', 1: 'Stage I', 2: 'Stage II', 3: 'Stage III', 4: 'Stage IV', 5: 'interpolation'}
    datas = data[data.columns[1:-4]].values
    samples = data[data.columns[0]].values
    N, D = np.shape(datas)

    mutation_data = pd.read_excel('key_gene_mutation.xlsx')
    mutation_sample = mutation_data.columns.to_list()

    landscape_data = pd.read_excel('landscape_data.xlsx')
    labs_landscape = landscape_data['labs'].values
    # 计算正常人中心
    normal_x_ave = 0
    normal_y_ave = 0
    normal_z_ave = 0
    count = 0
    for i in range(len(labs_landscape)):
        if labs_landscape[i] == 0:
            normal_x_ave = normal_x_ave + landscape_data['x'].values[i]
            normal_y_ave = normal_y_ave + landscape_data['y'].values[i]
            normal_z_ave = normal_z_ave + landscape_data['z'].values[i]/40
            count = count + 1
    normal_x_ave = normal_x_ave/count
    normal_y_ave = normal_y_ave/count
    normal_z_ave = normal_z_ave/count
    print(normal_x_ave, normal_y_ave, normal_z_ave)
    normal_coordinate = [normal_x_ave, normal_y_ave, normal_z_ave]
    normal_coordinate = np.array(normal_coordinate)


    # 计算每个病人的熵
    stage_weights = stage_normalization_weight_calculate(datas, labs)
    entropy_list = stage_normalization_entropy_calculate(datas, stage_weights, labs)
    entropy_list = np.array(entropy_list)

    # SOM的训练
    X = 30
    Y = 20
    weights = train_SOM(X=X, Y=Y, N_epoch=500, datas=datas, sigma=1.5, init_weight_fun=weights_PCA)

    workbook = xlwt.Workbook(encoding="utf-8")  # 创建workbook对象
    worksheet = workbook.add_sheet("sample_map")  # 创建工作表

    index = 0
    worksheet.write(index, 0, 'samples')
    worksheet.write(index, 1, 'x')
    worksheet.write(index, 2, 'y')
    worksheet.write(index, 3, 'coordinate')
    worksheet.write(index, 4, 'mutation_num')
    worksheet.write(index, 5, 'labs')
    worksheet.write(index, 6, 'pseudo_time')
    for i in range(N):
        if labs[i] != 0:
            temporary_node_x, temporary_node_y = get_winner_index(datas[i], weights)
            temporary_node = (temporary_node_x, temporary_node_y)
            temporary_samplename = ''
            for j in range(len(samples[i])):
                if j != 4 and j != 7:
                    temporary_samplename = temporary_samplename + samples[i][j]
            temporary_samplename = temporary_samplename + '01'
            if temporary_samplename in mutation_sample:
                index = index + 1
                temporary_coordinate = [temporary_node_x, temporary_node_y, landscape_data['z'].values[temporary_node_x + 30 * temporary_node_y + 1]/40]
                temporary_coordinate = np.array(temporary_coordinate)
                mutation_sum = mutation_data[temporary_samplename].values[-1]
                pseudo_time = np.linalg.norm(normal_coordinate - temporary_coordinate)

                worksheet.write(index, 0, samples[i])
                worksheet.write(index, 1, int(temporary_node_x))
                worksheet.write(index, 2, int(temporary_node_y))
                worksheet.write(index, 3, str(temporary_node))
                worksheet.write(index, 4, int(mutation_sum))
                worksheet.write(index, 5, int(labs[i]))
                worksheet.write(index, 6, pseudo_time)

    workbook.save("sample_pseudo_time.xls")
