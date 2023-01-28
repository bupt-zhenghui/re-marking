import os
import time


def get_cur_time(seg=':'):
    t = time.localtime()
    date = str(t.tm_year) + '-' + str(t.tm_mon).zfill(2) + '-' + str(t.tm_mday).zfill(2)
    return date + ' ' + str(t.tm_hour).zfill(2) + seg + str(t.tm_min).zfill(2) + seg + str(t.tm_sec).zfill(2)


def cur_date(seg='-'):
    t = time.localtime()
    return str(t.tm_year) + seg + str(t.tm_mon).zfill(2) + seg + str(t.tm_mday).zfill(2)


def get_ihd_data(dataset_root, is_train=True):
    image_path = []
    dataset_name = ['HAdobe5k', 'HCOCO', 'Hday2night', 'HFlickr']
    for dataset in dataset_name:
        dataset_dir = dataset_root + '/' + dataset + '/'
        assert os.path.isdir(dataset_dir), "ERROR: Make sure {} is in IHD Dataset directory".format(dataset)
        train_file = dataset_dir + dataset + ('_train.txt' if is_train else '_test.txt')
        with open(train_file, 'r') as f:
            for line in f.readlines():
                image_path.append(os.path.join(dataset_dir, 'composite_images', line.rstrip()))
    return image_path


def get_re_data(dataset_root):
    reg_path = './static/referring/iharmony_ref_reg.txt'
    caption_path = './static/referring/iharmony_ref_caption.txt'
    re_dic = {}
    with open(reg_path, 'r') as f:
        line = f.readline().strip()
        while line:
            mask, prompts = line.split('\t')
            mask = os.path.join(dataset_root, mask)
            re_dic[mask] = prompts.split(';')
            line = f.readline().strip()

    with open(caption_path, 'r') as f:
        line = f.readline().strip()
        while line:
            mask, caption = line.split('\t')
            mask = os.path.join(dataset_root, mask)
            re_dic[mask].append(caption)
            line = f.readline().strip()
    return re_dic


def get_iou_data(dataset_root):
    iou_path = 'static/referring/iou.txt'
    iou_dic = {}
    with open(iou_path, 'r') as f:
        line = f.readline().strip()
        while line:
            mask, points = line.split('\t')
            mask = os.path.join(dataset_root, mask)
            points = points.split(';')
            iou_dic[mask] = points
            line = f.readline().strip()
    f.close()
    return iou_dic


def get_sample_data(dataset_root):
    paths = get_ihd_data(dataset_root, True) + get_ihd_data(dataset_root, False)
    samples = []
    mask_st = set()
    for path in paths:
        mask, real = get_mask_real_path(path)
        if mask in mask_st: continue
        mask_st.add(mask)
        samples.append([mask, real])
    return samples


def get_mask_real_path(path):
    name_parts = path.split('_')
    mask_path = path.replace('composite_images', 'masks')
    mask_path = mask_path.replace(('_' + name_parts[-1]), '.png')
    target_path = path.replace('composite_images', 'real_images')
    target_path = target_path.replace(('_' + name_parts[-2] + '_' + name_parts[-1]), '.jpg')
    return mask_path, target_path


def test():
    prefix = '/workspace/dataset/Image_Harmonization_Dataset/'
    iou_dic = get_iou_data()
    for k, v in iou_dic.items():
        mask = k[len(prefix):]
        value = ';'.join(v)
        with open('static/referring/iou.txt', 'a') as f:
            f.write(mask + '\t' + value + '\n')
        f.close()


if __name__ == '__main__':
    dataset_dir = '/Users/zhenghui/Downloads/Image_Harmonization_Dataset'
    iou_dic = get_iou_data(dataset_dir)
    re_dic = get_re_data(dataset_dir)
    for k, v in iou_dic.items():
        if len(v) != len(re_dic[k]): print('False!')
    print('complete!')
