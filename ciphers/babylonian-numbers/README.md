# Babylonian Numerals
Tool to convert babylonian numbers (Babylonian Numerals). The Mesopotamian numeral system uses a mix of base 60 (sexagesimal) and base 10 (decimal) by writing wedges (vertical or corner wedge).

#### Charset: `0123456789ABCDE`

#### Tags: `babylonian, mesopotamian, numeral, babylon, cuneiform, writing, civilization, wedge, bracket, pipe, bar, arabic, roman`

#### Source: https://www.dcode.fr/babylonian-numbers

![combined](./combined.png)

### Questions

### How to write babylonian numbers?
In mesopotamian/babylonian number system, numbers have to be converted to base 60. Numbers are written in a cuneiform style with | and . Each vertical bar | (pipe) equals a unit and each  (corner wedge or bracket) equals a tenth. The change of power of sixty (60 ^ 1 = 60, 60 ^ 2 = 3600, 30 ^ 3 = 216000, etc.) is represented by a space. Example: 23 is written with 2 tenths and 3 units so  or  Example: 61 is written 1 sixtieth and 1 unit as | | or  (with a space separator) dCode uses the recent system (from the 3rd century civilization in Babylon) which introduce the writing or 0 (before the concept of zero did not exist, it was replace by an ambiguous empty space). Since Unicode 5 (2006) cuneiform symbols can be represented on compatible browsers, here is the table of characters used by dCode: 𒐕1𒐖2𒐗3𒐘4𒐙5𒐚6𒐛7𒐜8𒐝9𒌋10𒎙20𒌍30𒐏40𒐐50 NB: The double chevron character 𒎙 (20) has been forgotten in Unicode 5 (it existed as 《) and was added in Unicode 8 (2015) but may appear malformed on some operating systems.

### How to convert babylonian numbers?
Converting is easy by counting symbols and considering it in base 60 to get numbers into classical Hindu-Arabic notation. Example:  is 2  and 3 | so $ 2 \times 10 + 3 \times 1 = 23 $ Example: | | (note the space) is 1 | and then 1 | so $ 1 \times 60 + 1 = 61 $

### How to convert from base 10 to base 60?
TO convert a number $ n $ from base $ 10 $ to base $ b=60 $ apply the algorithm: $$ q_0=n; i=0; \mbox{ while } q_i > 0 \mbox{ do } (r_i = q_i \mbox{ mod } 60; q_{i+1}= q_i \mbox{ div } 60 ; i = i+1 ) $$ Example: $$ q_0 = 100 \\ r_0 = 100 \mbox{ mod } 60 = 40 \;\;\; q_1 = 100 \mbox{ div } 60 = 1 \\ r_1 = 1 \mbox{ mod } 60 = 1 \;\;\; q_2 = 0 \\ So \{1,0,0\}_{(10)} = \{1, 40\}_{(60)} $$

### How to write the number zero 0?
Babylonians did not use the zero (this concept had not been invented), but from the 3rd century they used the symbol

### How to count using Babylonian numerals?
Babylonian numbers chart (base60) 0 (zero)1234567891011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859 For other numbers, use the form above.

### Why the base 60?
60 has the advantage of having many divisors. Today the time system of hours still uses the base sixty: 60 seconds = 1 minute, 60 minutes = 1 hour = 3600 seconds

### How to convert Babylonian numbers into roman numerals?
Convert the Babylonian numbers to Hindu-Arabic numerals (1,2,3,4,5,6,7,8,9,0), then use the Roman numeral converter of dCode.

