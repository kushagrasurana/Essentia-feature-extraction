import essentia
from essentia.standard import *

import sys
from os import listdir
from os.path import isfile, join

def generate_central_moments(file, file_name, path):
	loader = essentia.standard.MonoLoader(filename = file)
	audio = loader()

	w = Windowing(type = 'hann')
	spectrum = Spectrum(size = 4096)
	central_moments = CentralMoments()
	distribution_shape = DistributionShape()
	pool = essentia.Pool()

	for frame in FrameGenerator(audio, frameSize = 2048, hopSize = 512):
	    c = central_moments(spectrum(w(frame)))
	    spread, skewness, kurtosis = distribution_shape(c)
	    #print("spread", spread, " skewness", skewness, "kurtosis", kurtosis)
        pool.add('lowlevel.spread', spread)
        pool.add('lowlevel.skewness', skewness)
        pool.add('lowlevel.kurtosis', kurtosis)

	output = YamlOutput(filename = join(path, 'spread_skewness_kurtosis', str(file_name) + '.json')
			 , format = 'json')
	output(pool)


def main():

	mypath = sys.argv[1]
	files = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
	file_names = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	
	for file, file_name in zip(files, file_names):
		generate_central_moments(file, file_name, mypath)


if __name__ == '__main__':
	main()