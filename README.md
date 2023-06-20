# Arithmetic-Encoding-Losless-Compression

## OVERVIEW 
Uses a basic Arithmetic Encoding algorithm to compress text.
Should at worse be the entropy + 2 bits so it is near optimal for compression (didn't verify this but I believe this is the case if the algorithm is correctly implemented). The reason you would use this over Hufman encoding is because if you have a large alphabet and a large file using Hufman would be impractical and probably infeasible.

## Limitations with the algorithm:
Due to the fact that we rely on hyper-accurate floating point calculations where exact accuracy is necessary the more precision needed the slower the algorithm will run and at a certain point theoretically infinite precision will be required. There are ways to mitigate this as I mention below in my improvements/to-do sections 

## NEEDED IMPROVEMENTS/TO-DO:
1. Can reduce the binary representation by truncating unneeded bits. Can take off all trailing bits as long as the binary representation is still in the range
2. Convert the result to an actual file text file compression can be implemented as it stands now the class can only generate a maximum nontruncated bitstream to represent the file.
3. Guarantee accuracy with alphabets with > 30 symbols so that the results are guaranteed to be accurate despite the inefficiency of floating point calculations. This can be done by either transforming the numbers into integers or we can immediately adding bits to our bit representation whenever the minimum and maximum share starting bits that way our interval does not continually shrink.
4. Add a place for the user to select decimal precision. 
5. Allow users to upload raw strings so we can generate a probability dictionary for them.
6. Allow users to pass in a .txt file and we can generate a binary file or give them the option to just receive either the binary representation or even the floating point representation before having it converted.
7. Split the decoder and encoder into separate classes
8. Should probably sort the dictionary in a specific way so it will always be the same
9. Add comments

## HOW THE ALGORITHM WORKS:
See the photo below or the worked example in the link above the image.
We have a number line from 0-1 and the probabilities of our alphabet are placed amongst the number line. When we read in character we limit the scope of our number line. We then split this section of the number line to conform to the same probabilities of our characters and each time we select a character the range shrinks. if A is within .5-.8 where .5 is the minimum and .8 is the maximum this range then is broken down. You can think of this range as our new number line so we break this section down further and place the probabilities of our characters within this range. This is why we essentially find a floating point representation of our string. 

https://www.youtube.com/watch?v=7vfqhoJVwuc&t=345s

https://cdncontribute.geeksforgeeks.org/wp-content/uploads/arithmetic.png


## HOW THE CODE WORKS:
1. create a class AE this will be our encoder/decoder. Must pass it the string and the probability take for now which is a dictionary where the key is the character and the value is the percentage that we will see that character.
2. when we call encode we set our Min and Max to 0 and 1 representing our number line. since we haven't read a character our range is the entire number line. We read in our string one character at a time and then call stage_encoder.
3. Stage encoder will take our dictionary values representing our probabilities and until we encounter the probability associated with the character we are reading we have to update our min or our max. Our range is Min - Max. This will stay the same through the calculations at this stage because we are trying to find our next range what we are adjusting is the Min and the Max within this range i.e where this probability for the character lies in our new number line (at each stage where we are calculating in an interval we can think of this as our new squeezed or compressed number line) so we add the current Min to the results of the interval multiplied by the probability to determine where it lies within this new number line
4. We do this until we have read all characters and then we call final_encoder which does the same thing as stage_encoder only now since we have no specific symbol we are looking for we want all probabilities within that range in order to find the absolute minimum within that interval and the absolute maximum within the final interval. We add them together and divide by two to get the floating point representation of our string
5. We then call to_binary in order to convert this to a binary string. Since it is a decimal we have to do binary expansion in order to get the representation
6. DECODING:
   We are doing the same thing as before but instead of a string what we are passing now is the encoded binary representation along with the length of the original string and the original probability distribution. We then do the same thing as we did for encoding only know we are transforming from binary to string

