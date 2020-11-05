# Music Sheet Cipher
Tool to decrypt/encrypt a music sheet paper notation. Each item/notes/symbol of a music sheet can be associated to a cipher letter or a digit.

#### Charset: `0123456ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`

#### Tags: `music, sheet, note, notation, book, instrument, sound, eighth, quarter, half, whole`

#### Source: https://www.dcode.fr/music-sheet-cipher

![combined](./combined.png)

### Questions

#### How to encrypt using a music sheet?
Encryption uses 14 notes and eighth notes, quarter notes, half note and whole note, this is 4*14=56 symbols + 3 extras. There are many ways to encode letters with these 59 symbols. dCode try common combinations in an automatic way and allows you to tell your own character list. Example: Example 1 : alphabet is composed of 14 eighth notes then the first 12 quarter notes : do1 = A, re1 = B, ... si1 = G, do2 = H, until sol2 = N then quarter notes do1 = O, etc. until fa2 = Z. Example: Example 2 : alphabet is composed of the first 13 eight notes then the 13 first quarter notes.

#### How to decrypt using a music sheet cipher?
The decryption of the Musical Sheet Cipher consists in the substitution of the 59 symbols (notes) by the characters of a defined alphabet.

#### How to recognize a music ciphertext?
The ciphered message is composed of classical notes without musical value. The notation used does not necessarily matter, no more than the instruments or actually produced sound. The sheet can be printed without a key or other important detail for a musician.

#### How to decipher music sheet without alphabet?
Try multiple alphabets and think to use a shifting cipher.

