import essentia
from essentia.standard import *

import sys
from os import listdir
from os.path import isfile, join

def generate_mfcc(file, file_name, path):
	loader = essentia.standard.MonoLoader(filename = file)
	audio = loader()

	w = Windowing(type = 'hann')
	spectrum = Spectrum(size = 4096)
	mfcc = MFCC()

	pool = essentia.Pool()

	for frame in FrameGenerator(audio, frameSize = 2048, hopSize = 512):
	    mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
	    pool.add('lowlevel.mfcc', mfcc_coeffs)

#	output = YamlOutput(filename = join(path, 'mfcc', str(file_name) + '.sig'), format = 'json')
#	output(pool)

	aggrPool = PoolAggregator(defaultStats = [ 'mean', 'var' ])(pool)
	output = YamlOutput(filename = join(path, 'mfcc', str(file_name) + '.json'), format = 'json')
	output(aggrPool)
	del pool
	del aggrPool
	del output


def main():

	mypath = sys.argv[1]
	files = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
	file_names = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	
	for file, file_name in zip(files, file_names):
		generate_mfcc(file, file_name, mypath)


if __name__ == '__main__':
	main()