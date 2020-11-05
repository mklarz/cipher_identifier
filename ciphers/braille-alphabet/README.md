# Braille Alphabet
Tools to write/translate Braille. Braille is a tactile alphabet/writing system for blind people that also can be described with digits.

#### Charset: ` !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`

#### Tags: `braille, louis, code, tactile, touch, finger, alphabet, blind, dot`

#### Source: https://www.dcode.fr/braille-alphabet

![combined](./combined.png)

### Questions

#### How to encrypt using Braille cipher?
Braille translation uses a specific alphabet for visually impaired/blind people, composed of dots suitable for touching with 1 or more fingers. Each letter corresponds to a combination of 6 dots (embossed or not). There are 2 major types of alphabets, the International alphabet and the French alphabet (which has specificities, for accented characters or numbers). Example: BRAILLE is written '⠃ ⠗ ⠁ ⠊ ⠇ ⠇ ⠑' (Unicode characters) or  (images) The dots are read in column and are numbered 1-2-3 for the first column and 4-5-6 for the second. Example: BRAILLE can therefore also be written 12,1235,1,24,123,123,15 For the digits, there are 2 modes, the international mode uses the symbol ⠼ (3-4-5-6 - backward L) and the letters from A to J are respectively 1,2,3,4,5,6,7,8,9 and 0. The second French mode, called Antoine, uses the symbol ⠠ (6) instead of ⠼ but keeps the letters from A to J for the value of the digits. Example: 1 is thus written ⠼⠁ (international mode) or ⠠⠁ (Antoine mode) An ambiguity can arise on the interpretation of the numbers with several digits '⠼⠁ ⠁' can mean 11 or 1A, to avoid this the numeric symbol ⠼ can be repeated with each digit. braille" loading="lazy" />

#### How to decrypt Braille cipher?
Braille decryption requires only a substitution with a Braille alphabet symbol (6 dots). Example:  or 145 14 135 145 15 is decrypted DCODE For digits, pay attention to the potential prefix ⠼ (3456) or ⠠ (6)

#### How to recognize Braille ciphertext?
The ciphered message is constituted of dots lined in 2 columns of 3 dots. Caution, however, it may be presented in forms unsuited to tactile reading (see variants).

#### What are the variants of the Braille cipher?
Depending on the languages some rare characters like those with accents can become other characters. Braille can be presented in Unicode characters, in numeric code (composed of numbers from 1 to 6 in groups), or in binary format (each digit from 1 to 6 can be rated by a bit 0 or 1). Example: D is coded 145 or 100110 (bits 1,4,5 are at 1, starting from the left) The 6 bits can be used in octal format (reverse reading in groups of 3 001 for 1, 011 for 3 to get 13).

#### How to print Braille?
Braille printing can be done with an embosser. More recently, 3D printing, although much longer, allows you to make your own braille prints. According to the Braille Authority, a Braille dot must have a diameter of 1.44 mm and a height of 0.48 mm. The distance between 2 points of the same character (horizontally or vertically) must be 2.34 mm. While the center distance between 2 identical points of 2 consecutive characters must be 6.20 mm. here (link)

#### When Braille have been invented?
Louis Braille presented it in 1829

