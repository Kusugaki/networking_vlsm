

import copy

class VLSM:
    MAX = bin(255)

    def __init__(self, name, ip, subnet_mask):
        self.name = name
        self.ip = ip
        self.subnet_mask = subnet_mask

        self.startingIP = ip
        self.startingSubnet = subnet_mask

        self.nextCityIP = ""
        self.nextCitySubnet = 0



    def calculate(self, required_subnets:list[int]):
        UsedHosts   = self.get_required_subnet(required_subnets)
        hostBits    = self.get_host_bits(UsedHosts)
        networkBits = 32 - hostBits
        Octet       = self.get_octet_index(networkBits)
        MagicNumber = self.get_magic_number(networkBits)
        
        NetworkIP   = self.split_IP(self.ip)
        FirstIP     = self.determine_first_IP(NetworkIP)
        BroadcastIP = self.determine_broadcast_IP(NetworkIP, Octet, MagicNumber)
        LastIP      = self.determine_last_IP(BroadcastIP)

        self.nextCityIP = self.determine_next_city_IP(BroadcastIP)
        self.nextCitySubnet = networkBits

        print(f"""
        {UsedHosts    = }
        {hostBits     = }
        {networkBits  = }
        {Octet + 1    = }
        {MagicNumber  = }

        {NetworkIP      = }
        {FirstIP        = }
        {LastIP         = }
        {BroadcastIP    = }
        SubnetMask     = {networkBits}

        {self.nextCityIP     = }
        {self.nextCitySubnet = }
        """)

    def __str__(self):
        return self.name


    def get_required_subnet(self, actualHosts:list[int] ) -> str:
        total_city_hosts:dict[int:int] = {}

        print(self.__str__(), "\n")
        
        # TURN LIST INTO DICTIONARY
        for i in actualHosts: total_city_hosts[i] = 0

        for requiredHosts in actualHosts:
            total_host:int = 0
            i = 0
            while True:
                total_host = 2**i
                if total_host > requiredHosts:
                    break
                i += 1
            total_city_hosts[requiredHosts] = total_host - 2

            print(f"{requiredHosts = }, actualHosts 2^{i}-2 = {total_city_hosts.get(requiredHosts)}")
        

        return sum(total_city_hosts.values())
    

    def get_host_bits(self, requiredHosts) -> int:
        i = 1
        hostCount = 0
        while True:
            hostCount = 2**i
            if hostCount > requiredHosts:
                break
            i += 1
        return i
    

    def get_octet_index(self, bits) -> int:
        if bits <= 8:    return 0
        elif bits <= 16: return 1
        elif bits <= 24: return 2
        else:            return 3


    def get_magic_number(self, networkBits) -> int:
        # GET NETWORK BIT REMAINDER
        modulo_bits = networkBits % 8
        
        if modulo_bits == 0:
            return 128
        
        # REVERSE THE COUNT TO MAKE IT GO RIGHT TO LEFT
        modulo_bits = 8 - modulo_bits
        
        magic_num = 0
        for i in range(modulo_bits+1):
            magic_num = 2**i

        return magic_num
    


    def split_IP(self, ip) -> list[int]:
        ip = ip.split(".")
        for i in range(len(ip)):
            ip[i] = int(ip[i])
        return ip
    

    def determine_first_IP(self, network_ip):
        firstIP = copy.deepcopy(network_ip)
        for i in range(1, len(firstIP)):
            if firstIP[-i] != 255:
                firstIP[-i] += 1
                break
        return firstIP
    

    def determine_last_IP(self, broadcast_ip):
        lastIP = copy.deepcopy(broadcast_ip)
        lastIP[-1] -= 1
        return lastIP


    def determine_broadcast_IP(self, ip, starting_octet_index, magic_number):
        broadcastIP = copy.deepcopy(ip)
        for i in range(starting_octet_index, len(broadcastIP)):
            if i == starting_octet_index:
                broadcastIP[i] += magic_number - 1
                if broadcastIP[i] > 255:
                    remainder = broadcastIP[i] % 255
                    broadcastIP[i] = remainder
                    broadcastIP[i-1] += 1
            else:
                broadcastIP[i] = 255
        return broadcastIP

            

    def determine_next_city_IP(self, broadcast_ip):
        nextIP = copy.deepcopy(broadcast_ip)
        for i in range(1, len(nextIP)):
            if nextIP[-i] == 255:
                nextIP[-i] = 0
                continue
            nextIP[-i] += 1
            break

        for i in range(len(nextIP)):
            nextIP[i] = str(nextIP[i])
        return ".".join(nextIP)
        

def assignment():
    starting_ip:str          = "10.0.0.0"
    starting_subnet_mask:int = 8


    # AAAAAAAAAAAAAAAAAAAAA
    LOCATION1 = VLSM("LOCATION1", starting_ip, starting_subnet_mask)
    LOCATION1.calculate([5001, 1999])

    #### CITIES

    LOCATION1_A = VLSM("LOCATION1_A", LOCATION1.startingIP, LOCATION1.startingSubnet)
    LOCATION1_A.calculate([5001])
    print(LOCATION1_A.nextCityIP)

    LOCATION1_B = VLSM("LOCATION1_B", LOCATION1_A.nextCityIP, LOCATION1_A.nextCitySubnet)
    LOCATION1_B.calculate([1999])

    # BBBBBBBBBBBBBBBBBBBBBBBB
    LOCATION2 = VLSM("LOCATION2", LOCATION1.nextCityIP, LOCATION1.nextCitySubnet)
    LOCATION2.calculate([5000, 700])

    #### CITIES

    LOCATION2_A = VLSM("LOCATION2_A", LOCATION2.startingIP, LOCATION2.startingSubnet)
    LOCATION2_A.calculate([5000])

    LOCATION2_B = VLSM("LOCATION2_B", LOCATION2_A.nextCityIP, LOCATION2_A.nextCitySubnet)
    LOCATION2_B.calculate([700])

    # CCCCCCCCCCCCCCCCCCCCCCCCC
    LOCATION3 = VLSM("LOCATION3", LOCATION2.nextCityIP, LOCATION2.nextCitySubnet)
    LOCATION3.calculate([4000, 900])

    #### CITIES

    LOCATION3_A = VLSM("LOCATION3_A", LOCATION3.startingIP, LOCATION3.startingSubnet)
    LOCATION3_A.calculate([4000])

    LOCATION3_B = VLSM("LOCATION3_B", LOCATION3_A.nextCityIP, LOCATION3_A.nextCitySubnet)
    LOCATION3_B.calculate([900])

    # DDDDDDDDDDDDDDDDDDDDDDDD
    LOCATION4 = VLSM("LOCATION4", LOCATION3.nextCityIP, LOCATION3.nextCitySubnet)
    LOCATION4.calculate([2400, 2000])

    #### CITIES

    LOCATION4_A = VLSM("LOCATION4_A", LOCATION4.startingIP, LOCATION4.startingSubnet)
    LOCATION4_A.calculate([2400])

    LOCATION4_B = VLSM("LOCATION4_B", LOCATION4_A.nextCityIP, LOCATION4_A.nextCitySubnet)
    LOCATION4_B.calculate([2000])

    # EEEEEEEEEEEEEEEEEEEEEEEEE
    LOCATION5 = VLSM("LOCATION5", LOCATION4.nextCityIP, LOCATION4.nextCitySubnet)
    LOCATION5.calculate([1200, 1010])

    #### CITIES

    LOCATION5_A = VLSM("LOCATION5_A", LOCATION5.startingIP, LOCATION5.startingSubnet)
    LOCATION5_A.calculate([1200])

    LOCATION5_B = VLSM("LOCATION5_B", LOCATION5_A.nextCityIP, LOCATION5_A.nextCitySubnet)
    LOCATION5_B.calculate([1010])

    del LOCATION1, LOCATION1_A, LOCATION1_B
    del LOCATION2, LOCATION2_A, LOCATION2_B
    del LOCATION3, LOCATION3_A, LOCATION3_B
    del LOCATION4, LOCATION4_A, LOCATION4_B
    del LOCATION5, LOCATION5_A, LOCATION5_B



def activity():
    starting_ip:str          = "10.0.0.0"
    starting_subnet_mask:int = 8


    Malaysia    = [79842, 9999]
    China       = [6999, 8686]
    Philippines = [6000, 3500, 2000, 1853, 1354, 1230, 1000]

    ASIA = VLSM("ASIA", starting_ip, starting_subnet_mask)
    '''
    Why [147452, 24572, 21490]? and not just a list of Malaysia + China + Philippines?
    Because Malaysia, with a total of 89,841 has the same subnet mask of the Entirity of ASIA
    MEANING, Malaysia takes ALL IP addresses of Asia and doesn't leave any leftovers for China 
    or Philippines. 

    Solution?

    Get the total requiredHosts for each city and get the sum, example:
                    City Hosts --> Actual Hosts
    ASIA:
        MALAYSIA:
            KL:         79842  --> 131070
            PETALING:   9999   --> 16382
                    SUM = 131070 + 16382 = 147,452
        CHINA:
            BEIJING:    8686   --> 16382
            WUHAN:      6999   --> 8190
                    SUM = 16382 + 8190   = 24572
        PHILIPPINES:
            DAVAO:      6000   --> 8190
            CEBU:       3500   --> 4094
            MAKATI:     2000   --> 2046
            ILOCOS:     1853   --> 2046
            CALAMBA:    1354   --> 2046
            CLARK:      1230   --> 2046
            MANILA:     1000   --> 1022
                    SUM = 8190 + 4094 + (2046*4) + 1022 = 21490
        
    Final total count to not have IP conflicts
    [147,452] + [24,572] + [21,490]

    hence the final answer of:
    ASIA.calculate([147452, 24572, 21490])
    and not:
        ASIA.calculate(Malaysia + China + Philippines)
            or
        ASIA.calculate([79842, 9999, 8686, 6999, 6000, 3500, 2000, 1853, 1354, 1230, 1000])
    '''
    ASIA.calculate([147452, 24572, 21490])

    ###### MALAYSIAAAAAAAAAAAAAAAA

    MALAYSIA = VLSM("MALAYSIA", ASIA.startingIP, ASIA.startingSubnet)
    MALAYSIA.calculate(Malaysia)

    ### CITIES

    KL = VLSM("KL", MALAYSIA.startingIP, MALAYSIA.startingSubnet)
    KL.calculate([79842])

    PETALING = VLSM("PETALING", KL.nextCityIP, KL.nextCitySubnet)
    PETALING.calculate([9999])

    ###### PHILIPPINESSSSSSSSSSSSSS

    PHILIPPINES = VLSM("PHILIPPINES", MALAYSIA.nextCityIP, MALAYSIA.nextCitySubnet)
    PHILIPPINES.calculate(Philippines)

    ### CITIES

    DAVAO = VLSM("DAVAO", PHILIPPINES.startingIP, PHILIPPINES.startingSubnet)
    DAVAO.calculate([6000])

    CEBU = VLSM("CEBU", DAVAO.nextCityIP, DAVAO.nextCitySubnet)
    CEBU.calculate([3500])

    MAKATI = VLSM("MAKATI", CEBU.nextCityIP, CEBU.nextCitySubnet)
    MAKATI.calculate([2000])

    ILOCOS = VLSM("ILOCOS", MAKATI.nextCityIP, MAKATI.nextCitySubnet)
    ILOCOS.calculate([1853])

    CALAMBA = VLSM("CALAMBA", ILOCOS.nextCityIP, ILOCOS.nextCitySubnet)
    CALAMBA.calculate([1354])

    CLARK = VLSM("CLARK", CALAMBA.nextCityIP, CALAMBA.nextCitySubnet)
    CLARK.calculate([1230])

    MANILA = VLSM("MANILA", CLARK.nextCityIP, CLARK.nextCitySubnet)
    MANILA.calculate([1000])

    ###### CHINAAAAAAAAAAAAAAAAAAAA

    CHINA = VLSM("CHINA", PHILIPPINES.nextCityIP, PHILIPPINES.nextCitySubnet)
    CHINA.calculate(China)

    ### CITIES
    
    BEIJING = VLSM("BEIJING", CHINA.startingIP, CHINA.startingSubnet)
    BEIJING.calculate([8686])

    WUHAN = VLSM("WUHAN", BEIJING.nextCityIP, BEIJING.nextCitySubnet)
    WUHAN.calculate([6999])

    ################################################3
    ################################################3
    ################################################3
    ################################################3

    Usa    = [5559, 4987, 342, 333, 321, 67]
    Canada = [2048, 510, 128, 254]

    NORTHAMERICA = VLSM("NORTH AMERICA", ASIA.nextCityIP, ASIA.nextCitySubnet)
    NORTHAMERICA.calculate([18036, 5112])

    ######### USAAAAAAAAAAAAAA
    
    USA = VLSM("USA", NORTHAMERICA.startingIP, NORTHAMERICA.startingSubnet)
    USA.calculate(Usa)

    ### CITIES

    IOWA = VLSM("IOWA", USA.startingIP, USA.startingSubnet)
    IOWA.calculate([5559])

    LA = VLSM("LA", IOWA.nextCityIP, IOWA.nextCitySubnet)
    LA.calculate([4987])

    WASHINGTON = VLSM("WASHINGTON", LA.nextCityIP, LA.nextCitySubnet)
    WASHINGTON.calculate([342])

    DETROIT = VLSM("DETROIT", WASHINGTON.nextCityIP, WASHINGTON.nextCitySubnet)
    DETROIT.calculate([333])

    NY = VLSM("NY", DETROIT.nextCityIP, DETROIT.nextCitySubnet)
    NY.calculate([321])

    UTAH = VLSM("UTAH", NY.nextCityIP, NY.nextCitySubnet)
    UTAH.calculate([67])


    ######### CANADAAAAAAAAAA

    CANADA = VLSM("CANADA", USA.nextCityIP, USA.nextCitySubnet)
    CANADA.calculate(Canada)

    ### CITIES

    VANCOUVER = VLSM("VANCOUVER", CANADA.startingIP, CANADA.startingSubnet)
    VANCOUVER.calculate([2048])

    QUEBEC = VLSM("QUEBEC", VANCOUVER.nextCityIP, VANCOUVER.nextCitySubnet)
    QUEBEC.calculate([510])

    # ONTARIO AND TORONTO HAS ERRORS WITH A DIRECT NETWORK PORTION DIVISIBLE BY 8
    # FALSE ANSWERS
    ONTARIO = VLSM("ONTARIO", QUEBEC.nextCityIP, QUEBEC.nextCitySubnet)
    ONTARIO.calculate([254])

    TORONTO = VLSM("TORONTO", ONTARIO.nextCityIP, ONTARIO.nextCitySubnet)
    TORONTO.calculate([128])

    del ASIA, MALAYSIA, KL, PETALING
    del CHINA, BEIJING, WUHAN
    del PHILIPPINES, DAVAO, CEBU, MAKATI, ILOCOS, CALAMBA, CLARK, MANILA
    del NORTHAMERICA, USA, IOWA, LA, WASHINGTON, DETROIT, NY, UTAH
    del CANADA, VANCOUVER, QUEBEC, ONTARIO, TORONTO


# MAIN PROGRAM
if __name__ == "__main__":
    assignment()

    activity()
