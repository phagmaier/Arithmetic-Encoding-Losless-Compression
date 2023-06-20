class AE:
    from decimal import Decimal
    def __init__(self,string,P):
        self.string = string
        self.P = P
    
    def stage_encoder(self,Min,Max,s):
        answer = None
        interval = Max - Min
        for key in self.keys:
            Max = interval * self.P[key] + Min
            answer = (Min,Max)
            Min = Max
            if key == s:
                return answer
    
    #used for when you need to get all probabiltieis 
    def final_encoder(self,Min,Max):
        answer = {}
        interval = Max - Min
        for key in self.keys:
            Max = interval * self.P[key] + Min
            answer[key] = (Min,Max)
            Min = Max
        return answer
    
    def get_decimal(self,dic):
        probs = []
        for i in dic.values():
            for x in i:
                probs.append(x)
        return (min(probs) + max(probs)/2), min(probs), max(probs)
    
    def float2bin(self, float_num, num_bits=None):

        float_num = str(float_num)
        if float_num.find(".") == -1:
            # No decimals in the floating-point number.
            integers = float_num
            decimals = ""
        else:
            integers, decimals = float_num.split(".")
        decimals = "0." + decimals
        decimals = Decimal(decimals)
        integers = int(integers)

        result = ""
        num_used_bits = 0
        while True:
            mul = decimals * 2
            int_part = int(mul)
            result = result + str(int_part)
            num_used_bits = num_used_bits + 1

            decimals = mul - int(mul)
            if type(num_bits) is type(None):
                if decimals == 0:
                    break
            elif num_used_bits >= num_bits:
                break
        if type(num_bits) is type(None):
            pass
        elif len(result) < num_bits:
            num_remaining_bits = num_bits - len(result)
            result = result + "0"*num_remaining_bits

        integers_bin = bin(integers)[2:]
        result = str(integers_bin) + "." + str(result)
        return result

    def bin2float(self,bin_num):
        if bin_num.find(".") == -1:
            # No decimals in the binary number.
            integers = bin_num
            decimals = ""
        else:
            integers, decimals = bin_num.split(".")
        result = Decimal(0.0)

        # Working with integers.
        for idx, bit in enumerate(integers):
            if bit == "0":
                continue
            mul = 2**idx
            result = result + Decimal(mul)

        # Working with decimals.
        for idx, bit in enumerate(decimals):
            if bit == "0":
                continue
            mul = Decimal(1.0)/Decimal((2**(idx+1)))
            result = result + mul
        return result
    
    def process_stage_binary(self, float_interval_min, float_interval_max, stage_min_bin, stage_max_bin):

        stage_mid_bin = stage_min_bin + "1"
        stage_min_bin = stage_min_bin + "0"

        stage_probs = {}
        stage_probs[0] = [stage_min_bin, stage_mid_bin]
        stage_probs[1] = [stage_mid_bin, stage_max_bin]

        return stage_probs
    
    def to_binary(self, float_interval_min, float_interval_max):
        
        #binary_encoder = []
        binary_code = None

        stage_min_bin = "0.0"
        stage_max_bin = "1.0"

        stage_probs = {}
        stage_probs[0] = [stage_min_bin, "0.1"]
        stage_probs[1] = ["0.1", stage_max_bin]
        
        while True:
            if float_interval_max < self.bin2float(stage_probs[0][1]):
                stage_min_bin = stage_probs[0][0]
                stage_max_bin = stage_probs[0][1]
            else:
                stage_min_bin = stage_probs[1][0]
                stage_max_bin = stage_probs[1][1]


            stage_probs = self.process_stage_binary(float_interval_min,
                                                    float_interval_max,
                                                    stage_min_bin,
                                                    stage_max_bin)

            if (self.bin2float(stage_probs[0][0]) >= float_interval_min) and (self.bin2float(stage_probs[0][1]) < float_interval_max):
                binary_code = stage_probs[0][0]
                break
            elif (self.bin2float(stage_probs[1][0]) >= float_interval_min) and (self.bin2float(stage_probs[1][1]) < float_interval_max):
                binary_code = stage_probs[1][0]
                break
        return binary_code
    
    def encode(self):
        Min = 0
        Max = 1
        #ensuring that they will always be in the same order
        self.keys = list(P.keys())
        for s in self.string:
            Min,Max = self.stage_encoder(Min,Max,s)
        final = self.final_encoder(Min,Max)
        answer,Min,Max = self.get_decimal(final)
        return self.to_binary(Min,Max)
    
    
    
    def stage_decoder(self,P,Min,Max):
        answer = {}
        interval = Max - Min
        for key in P.keys():
            Max = interval * Decimal(P[key]) + Min
            answer[key] = (Min,Max)
            Min = Max
        return answer
    
    
    
    
    def decode(self, encoded_msg, msg_length, probability_table):
        decoded_msg = []

        stage_min = Decimal(0.0)
        stage_max = Decimal(1.0)

        for idx in range(msg_length):
            #need to change this so it returns the min and the max
            stage_probs = self.stage_decoder(probability_table, stage_min, stage_max)

            for msg_term, value in stage_probs.items():
                if encoded_msg >= value[0] and encoded_msg <= value[1]:
                    break

            decoded_msg.append(msg_term)

            stage_min = stage_probs[msg_term][0]
            stage_max = stage_probs[msg_term][1]

        return decoded_msg
        