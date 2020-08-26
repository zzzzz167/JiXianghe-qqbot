import os

def getCPUtemperature():
    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp)/1000

def getDiskSpace():
        p = os.popen("df -h /")
        i = 0
        while 1:
            i = i +1
            line = p.readline()
            if i==2:
                return(line.split()[1:5])
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))
def zhu():
    CPU_temp = getCPUtemperature()
    CPU_usage = getCPUuse()
 
# RAM information
# Output is in kb, here I convert it in Mb for readability
    RAM_stats = getRAMinfo()
    #RAM_total = round(int(RAM_stats[0]) / 1000,1)
    #RAM_used = round(int(RAM_stats[1]) / 1000,1)
    RAM_free = round(int(RAM_stats[2]) / 1000,1)
 
# Disk information
    DISK_stats = getDiskSpace()
    #DISK_total = DISK_stats[0]
    DISK_used = DISK_stats[1]
    #DISK_perc = DISK_stats[3]
    printf = "现在洮洮的体表温度为：" + str(CPU_temp)+"\n洮洮的脑袋占用：" + str(CPU_usage)+"\n洮洮可用的缓存："+str(RAM_free)+"\n洮洮已经占用的记忆："+str(DISK_used)
    return printf
#print(zhu())
