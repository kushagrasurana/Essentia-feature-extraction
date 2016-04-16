import essentia
from essentia.standard import *

import sys
from os import listdir
from os.path import isfile, join

def generate_flatness(file, file_name, path):
	loader = essentia.standard.MonoLoader(filename = file)
	audio = loader()

	w = Windowing(type = 'hann')
	spectrum = Spectrum()
	flatness = Flatness()

	pool = essentia.Pool()

	for frame in FrameGenerator(audio, frameSize = 2048, hopSize = 512):
	    c = flatness(spectrum(w(frame)))
        pool.add('lowlevel.flatness', c)

	output = YamlOutput(filename = join(path, 'flatness', str(file_name) + '.json'), format = 'json')
	output(pool)


def main():

	mypath = sys.argv[1]
	files = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
	file_names = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	
	for file, file_name in zip(files, file_names):
		generate_flatness(file, file_name, mypath)


if __name__ == '__main__':
	main()