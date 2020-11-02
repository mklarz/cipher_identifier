# dcode.fr cipher identifier
WIP of a script that tries to identify symbol ciphers (for now) available on [dcode.fr](https://www.dcode.fr/) based on input.

A compiled list of all of the image symbols can be found in [CIPHERS.md](CIPHERS.md).

#### Install
```
git clone https://github.com/corax/dcode_identifier.git`
cd ./dcode_identifier
pip install -r requirements.txt
CC="cc -mavx2" pip install -U --force-reinstall pillow-simd
```

#### Requirements
- python3
- [opencv-python](https://pypi.org/project/opencv-python/)
- [requests](https://pypi.org/project/requests/)

#### Running
```
$ find_cipher.py ./tests/betamaze.png
Checking: ancients-stargate-alphabet = 0
Checking: arthur-invisibles-cipher = 0.151
Checking: atlantean-language = 0.351
Checking: aurebesh-alphabet = 0
Checking: babylonian-numbers = 0
--- snip ---
================================
Top ciphers:
1	0.821	pokemon-unown-alphabet
2	0.516	betamaze-cipher
3	0.41	maritime-signals-code
4	0.366	hylian-language-skyward-sword
5	0.351	atlantean-language
6	0.267	mary-stuart-code
7	0.255	hylian-language-twilight-princess
8	0.2	semaphore-trousers-cipher
9	0.187	ogham-alphabet
10	0.183	webdings-font
11	0.151	arthur-invisibles-cipher
12	0.142	templars-cipher
13	0.132	chinese-code
14	0.114	symbol-font
15	0.094	music-sheet-cipher
16	0.091	pigpen-cipher
17	0.089	wingdings-font
18	0.074	french-sign-language
19	0.073	draconic-dragon-language
20	0.064	lingua-ignota-code
================================
```

#### Scripts
##### `$ find_cipher.py <image>`
Compares the symbols of each cipher to the input image `<image>` and lists the the match probability.
Uses [OpenCV](https://opencv.org/) to look for matching symbols.

##### `$ scripts/download_images.py`
Downloads symbol pictures of each cipher and saves them to `./ciphers`, which also hosted in this repo.

##### `$ scripts/generate_combined_images.py`
Script that generates the combined images of each cipher found in [CIPHERS.md](CIPHERS.md) ./ciphers`.

##### `$ scripts/generate_ciphers_md.py`
Script that generates the [CIPHERS.md](CIPHERS.md) file based on ciphers found in `./ciphers`.

##### `$ scripts/generate_train_data.py`
Script that generates train data per cipher, for training model classifiers. Training data is placed in `./ciphers/<cipher>/train_data`.
