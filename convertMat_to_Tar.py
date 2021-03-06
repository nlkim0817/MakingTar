import sys
sys.path.append('..')
import logging
import random
import numpy as np
import scipy.io
from path import Path
import argparse
import npytar

def write(records, fname):
    writer = npytar.NpyTarWriter(fname)
    n = 0 ;
    for fname in records:
        name = '{:03d}.{}.{:03d}'.format(n, 'UCF', n)
        arr = scipy.io.loadmat(fname)['DB'].astype(np.float32)
        arrpad = np.zeros((64,)*3, dtype=np.float32)
        arrpad = arr 
	writer.add(arrpad, name)
    writer.close()



if __name__=='__main__': #data structure
	parser = argparse.ArgumentParser() #parsing directory
	parser.add_argument('data_dir', type=Path)
	args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s| %(message)s')
base_dir = (args.data_dir).expand()
records = {'train': [], 'test': []}
logging.info('Loading .mat files')
for fname in sorted(base_dir.walkfiles('*.mat')):
    if fname.endswith('test_feature.mat') or fname.endswith('train_feature.mat'):
        continue
    elts = fname.splitall() #if you need to parse any keywords from file name, 
    split = elts[2]
    records[split].append(fname)


# just shuffle train set
logging.info('Saving train npy tar file')
train_records = records['train']
random.shuffle(train_records)
write(train_records, 'ucf101_train.tar')

# order test set by instance and orientation
logging.info('Saving test npy tar file')
test_records = records['test']
test_records = sorted(test_records, key=lambda x: x[2])
test_records = sorted(test_records, key=lambda x: x[1])
write(test_records, 'ucf101_test.tar')
