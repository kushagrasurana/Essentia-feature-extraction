import sys
from concurrent.futures import ProcessPoolExecutor
from os import listdir, makedirs
from os import path

sys.path.insert(0, './essentia-scripts/')
from spread import generate_spread
from skewness import generate_skewness
from kurtosis import generate_kurtosis
from flatness import generate_flatness
from loudness import generate_loudness
from mfcc import generate_mfcc
from roll_off import generate_roll_off
from spectral_centroid import generate_spectral_centroid
from zero_crossing_rate import generate_zero_crossing_rate

mypath = sys.argv[1]
features = ['centroid', 'flatness', 'loudness', 'mfcc', 'roll_off', 'spread', 'skewness', 'kurtosis', 'zero_crossing_rate']
genres = [path.join(mypath, "Carnatic/"), path.join(mypath, "Filmy/"), path.join(mypath, "Ghazal/"), path.join(mypath, "Hindustani/")]
functions = [generate_skewness, generate_spread, generate_kurtosis, generate_flatness, generate_loudness, generate_mfcc,
			 generate_roll_off, generate_spectral_centroid, generate_zero_crossing_rate]

def create_dirs():
	for genre in genres:
		for feature in features:
			if not path.exists(path.join(genre, feature)):
				makedirs(path.join(genre, feature))

def generate_data():
	for genre in genres:
		files = [path.join(genre, f) for f in listdir(genre) if path.isfile(path.join(genre, f))]
		file_names = [f for f in listdir(genre) if path.isfile(path.join(genre, f))]
		
		for file, file_name in zip(files, file_names):
			for function in functions:
				with ProcessPoolExecutor(max_workers=1) as executor:
				    executor.submit(function, file, file_name, genre)
				#function(file, file_name, genre)

def main():
	create_dirs()
	generate_data()

if __name__ == '__main__':
	main()