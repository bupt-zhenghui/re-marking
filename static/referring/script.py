import os
import utils

dataset_dir = '/Users/zhenghui/Downloads/Image_Harmonization_Dataset/'
tmp_dir = '/workspace/dataset/Image_Harmonization_Dataset/'
mask_dic = {}

for path in ['iharmony_ref_caption_train.txt', 'iharmony_ref_caption_test.txt']:
    with open(path, 'r') as f:
        line = f.readline().strip()
        while line:
            if len(line.split('\t')) == 2:
                k, v = line.split('\t')
                mask_dic[k] = v
            line = f.readline().strip()
print(f'length: {len(mask_dic)}')

with open('./iharmony_ref_caption.txt', 'a') as f:
    for k, v in mask_dic.items():
        f.write(k[len(tmp_dir):] + '\t' + v + '\n')
f.close()
