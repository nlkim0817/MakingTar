from path import Path
import argparse
import npytar

if __name__=='__main__': #data structure
   parser = argparse.ArgumentParser() #parsing directory
   parser.add_argument('tar_fn', type=Path)
   args = parser.parse_args()

reader = npytar.NpyTarReader(args.tar_fn)
for ix, (x, name) in enumerate(reader):
   print ('Data Name : %s, Index : %d' %(name,ix))
   print (x.shape)
        
