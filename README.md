# Arithmetic-Encoding-Losless-Compression

## OVERVIEW 
Uses a basic Arithmetic Encoding algorithm to compress text.
Should at worse be the entropy + 2 bits so it is near optimal for compression. 

## NEEDED IMPROVEMENTS/TO-DO:
1. Can reduce the binary representation by truncating unneeded bits. Can take off all trailing bits as long as the binary representation is still in the range
2. Convert the result to an actual file text file compression can be implemented as it stands now the class can only generate a maximum nontruncated bitstream to represent the file.
3. Guarantee accuracy with alphabets with > 30 symbols so that the results are guaranteed to be accurate despite the inefficiency of floating point calculations. This can be done by either transforming the numbers into integers or we can immediately adding bits to our bit representation whenever the minimum and maximum share starting bits that way our interval does not continually shrink.
4. Add a place for the user to select decimal precision. 
5. Allow users to upload raw strings so we can generate a probability dictionary for them.
6. Allow users to pass in a .txt file and we can generate a binary file or give them the option to just receive either the binary representation or even the floating point representation before having it converted. 
