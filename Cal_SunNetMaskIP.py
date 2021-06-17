def findePrefix(hostIp):
    pow = 0
    while(True):
        if (hostIp == 2):         # 2 is router
            calHostIp = hostIp+2  # +2 is  ipNetwork, ipbroadcast
        else:
            calHostIp = hostIp+3  # +3 is ipGateWay, ipNetwork, ipbroadcast

        if (2**pow >= calHostIp):
            prefix = 32 - pow
            bit = pow
            host = 2**pow
            return (prefix, bit, host)
        pow += 1


def calPrefix(numberHostIP, sort=True):
    if (sort == True):
        numberHostIP.sort(reverse=True)
    lst = [findePrefix(i) for i in numberHostIP]

    print("prefix:")
    for i, prefix in enumerate(lst):
        print("{:4}\t: /{}\t\t{}bit\t{:3}host".format(
            numberHostIP[i], prefix[0], prefix[1], prefix[2]))
    hostAll = [host[2] for host in lst]
    print("\nlen\t:", (len(numberHostIP)))
    print("hostsum\t:", (sum(hostAll)))

    return lst  # listOftuple  data about calculation of prefix


def calNetMask(prefix, base="D"):
    netMaskBin = ""
    for i in range(32):
        if (i % 8 == 0 and i != 0):
            netMaskBin += "."
        if (i < prefix):
            netMaskBin += "1"
        else:
            netMaskBin += "0"

    netMaskDec = []
    for i in netMaskBin.split("."):
        netMaskDec.append(str(int(i, 2)))
    netMaskDec = ".".join(netMaskDec)
    if (base.upper() == "D"):
        return netMaskDec
    elif (base.upper() == "B"):
        return netMaskBin
    else:
        raise Exception(
            "base, not correct  ex. ---> (prerix,[option])    option input ---->  D  or B ")


def calSubnetIp(ipStr, prefix1, prefix2, i):
    prefix1 = int(prefix1)
    prefix2 = int(prefix2)
    addPerTime = 2**(32-prefix2)
    ip = ipStr.split(".")
    ip = [int(i) for i in ip]

    addSumPerTime = (addPerTime) * (i-1)
    lct1 = int(addSumPerTime/16777216)
    addSumPerTime = int(addSumPerTime % 16777216)
    lct2 = int(addSumPerTime/65536)
    addSumPerTime = int(addSumPerTime % 65536)
    lct3 = int(addSumPerTime/256)
    addSumPerTime = int(addSumPerTime % 256)
    lct4 = int(addSumPerTime)

    Network = []
    Network.append(ip[0]+lct1)
    Network.append(ip[1]+lct2)
    Network.append(ip[2]+lct3)
    Network.append(ip[3]+lct4)

    addSumPerTime = (addPerTime)-1
    lct1 = int(addSumPerTime/16777216)
    addSumPerTime = int(addSumPerTime % 16777216)
    lct2 = int(addSumPerTime/65536)
    addSumPerTime = int(addSumPerTime % 65536)
    lct3 = int(addSumPerTime/256)
    addSumPerTime = int(addSumPerTime % 256)
    lct4 = int(addSumPerTime)

    Broadcast = []
    Broadcast.append(Network[0]+lct1)
    Broadcast.append(Network[1]+lct2)
    Broadcast.append(Network[2]+lct3)
    Broadcast.append(Network[3]+lct4)

    FirstIP = Network.copy()
    FirstIP[3] += 1

    LastIP = Broadcast.copy()
    LastIP[3] -= 1

    Network = [str(i) for i in Network]
    Broadcast = [str(i) for i in Broadcast]
    FirstIP = [str(i) for i in FirstIP]
    LastIP = [str(i) for i in LastIP]

    Network = ".".join(Network)
    Broadcast = ".".join(Broadcast)
    FirstIP = ".".join(FirstIP)
    LastIP = ".".join(LastIP)

    return {'network': Network, 'broadcast': Broadcast, 'firstIP': FirstIP, 'lastIP': LastIP}


def subNet(ip, prefix1, prefix2, dataIP, indexOfDataIP=0, indentation=0):
    prefix1 = int(prefix1)
    prefix2 = int(prefix2)
    # หาผลต่างของทั้ง 2 prefix เพื่อหาว่าห่างกันกี่ bit
    bit = abs(prefix1 - prefix2)
    numberOfIP = 2**bit  # จำนวนของ IP ที่ใช้ทำ subnet ได้

    for i in range(1, numberOfIP+1):

        if (i == 1 or i == numberOfIP):  # ถ้าเป็น ipแรก กับ ip สุดท้าย ถูกจำกัดไม่ให้ใช้
            if (i == 1):
                print("{}(/{} -> /{})\t/{} ={}".format("\t"*indentation,
                      prefix1, prefix2, prefix2, calNetMask(prefix2)))
            print("{}{:4}:=x".format("\t"*indentation, i))
            if (i == numberOfIP):
                return indexOfDataIP
        else:
            # ถ้าค่า index ยังไม่เกินจำนวนของข้อมูลdataIP ที่ต้องการแบ่ง subnet
            if (indexOfDataIP < len(dataIP)):

                if (prefix2 == dataIP[indexOfDataIP][0]):  # dataIP[i][0] is prefix
                    network = calSubnetIp(ip, prefix1, prefix2, i)['network']
                    broadcast = calSubnetIp(ip, prefix1, prefix2, i)['broadcast']
                    firstIP = calSubnetIp(ip, prefix1, prefix2, i)['firstIP']
                    lastIP = calSubnetIp(ip, prefix1, prefix2, i)['lastIP']
                    print("{}{:4}: {:12}\t={:4}".format("\t"*indentation,i, network, numberHostIP[indexOfDataIP]))
                    tableSubNetIP.append((numberHostIP[indexOfDataIP], network, broadcast, firstIP, lastIP, prefix2, calNetMask(prefix2)))  # createTable SunNetIP
                    indexOfDataIP += 1
                else:
                    # ต้องหาค่าผลต่างของ Prefix ก่อนเพื่อดักการทำ subnet ของ router เช่น 29-30 ได้ 1bit ซึ่งไม่ถูกต้องเพราะ router ต้องการ 2bit
                    if (abs(prefix2 - dataIP[indexOfDataIP][0]) > 1):
                        indentation += 1
                        print("--"*60)
                        network = calSubnetIp(ip, prefix1, prefix2, i)['network']
                        indexOfDataIP = subNet(network, prefix2, dataIP[indexOfDataIP][0], dataIP, indexOfDataIP, indentation)
                        indentation -= 1
                    else:
                        pass
                        # print("{}=_".format("\t"*indentation, i))
            else:
                pass
                # print("{}=_".format("\t"*indentation, i))


def ShowTableSunnetMask():
    print("Table Sunet IP")
    print("--"*60)
    print("{:3}\t{:13}\t{:13}\t{:13}\t{}\t\t/{}\t\t{}".format("Host","NetWork", "Broadcast", "FirestIP", "LastIP", "Prefix", "NetMask"))
    print("--"*60)
    for row in tableSubNetIP:
        # host  NetWork  Broadcast  FirstIP  LastIP  prefix  netmask
        print("{:3}\t{:13}\t{:13}\t{:13}\t{}\t/{}\t\t{}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))


def callUseSunnetIP(ip, prefix1, prefix2, numberHostIP, numberRouter):
    numberRouter = [2] * numberRouter
    numberHostIP += numberRouter
    dataIP = calPrefix(numberHostIP)
    print("\n\n")
    subNet(ip, prefix1, prefix2, dataIP)
    print("\n\n")
    ShowTableSunnetMask()


if __name__ == "__main__":
  tableSubNetIP = list()
  numberHostIP = [300, 61, 60, 33, 32, 5, 5, 4, 4] #ใส่ hostแต่ละอัน  ไม่รวม Router
  numberRouter = 3     #จำนวนRouter
  callUseSunnetIP("127.20.0.0", 21, 23, numberHostIP, numberRouter)  #ใส่ IP ที่ได้ พร้อมกับ /prefixเริ่ม to /prefixที่ต้องการแปลง