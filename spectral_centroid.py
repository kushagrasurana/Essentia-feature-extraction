import essentia
from essentia.standard import *

import sys
from os import listdir
from os.path import isfile, join

def generate_spectral_centroid(file, file_name, path):
	loader = essentia.standard.MonoLoader(filename = file)
	audio = loader()

	w = Windowing(type = 'hann')
	spectrum = Spectrum()
	centroid = Centroid()

	pool = essentia.Pool()

	for frame in FrameGenerator(audio, frameSize = 2048, hopSize = 512):
	    c = centroid(spectrum(w(frame)))
        pool.add('lowlevel.centroid', c)

	#output = YamlOutput(filename = join(path, 'centroid', str(file_name) + '.yaml'))
	#output(pool)

	aggrPool = PoolAggregator(defaultStats = [ 'mean', 'var' ])(pool)
	output = YamlOutput(filename = join(path, 'centroid', str(file_name) + '_aggr' + '.yaml'), format = 'json')
	output(aggrPool)


def main():

	mypath = sys.argv[1]
	files = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
	file_names = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	
	for file, file_name in zip(files, file_names):
		generate_spectral_centroid(file, file_name, mypath)


if __name__ == '__main__':
	main()