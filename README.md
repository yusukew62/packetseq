# packetseq
Create packet sequence diagram from pcap format csv file

[![Code Climate](https://codeclimate.com/repos/57ff5817e3bc270794005139/badges/1d9ff0fb1887c35cb28f/gpa.svg)](https://codeclimate.com/repos/57ff5817e3bc270794005139/feed)

## Description
Create the image file of the packet sequence diagram based on the multiple packet captured files.  
Input files uses the csv files made from the pcap files. Output file is the png file.

## Requirements
* Python 2.7
* setuptools
* seqdiag

## Install
```bash
$ pip install packetseq
```

## Usage

### Overview
1. Capture the network packets on the multiple network nodes  
2. Export the only communication of specific source port from the capture files using the wireshark  
3. Save as a CSV file
4. Send csv files to the environment having the packetseq
5. Run the packetseq
6. Enter the name of the other devices of communication from the standard input  
7. Output file is created

### Detail

Here, describe the following environment case
```text
Client (Windows 7) --- Proxy (Squid) --- Server (nifty.com)
```

#### 1. Capture the network packets on the multiple network nodes  

1. Capture the packets using the wireshark on the Windows 7  
(e.g., file name is client.pcap)
2. Capture the packets using the tcpdump on the Proxy Server  
(e.g., file name is proxy.pcap)

#### 2. Export the only communication of specific source port from the capture files using the wireshark  

1. Check the port number to squeeze the specific source port
2. Perform a filter on the wireshark  
```text
tcp.port == "soure port number"
```

#### 3. Save as a CSV file

Select the following colum on the wireshark
```text
"No.","Time","Source","Destination","Protocol","Length","Info"
```
Select the 'Date and Time of Day' in the 'Time Display Format' from menu
```text
1973-06-14 01:02:03.123456
```
Save as a csv file on the wireshark  
(e.g., file name are client.csv, proxy.csv)

#### 4. Send csv files to the environment having the packetseq

#### 5. Run the packetseq
```bash
$ packetseq client.csv proxy.csv
```

#### 6. Enter the name of the other devices of communication from the standard input  

Input the name  
(e.g., Windows 7 -> Client)
```text
########################################  
file_name:client.csv  
########################################  
src ip:192.168.1.3 -> src name: ???  
input src name > Client  
dst ip:192.168.1.62 -> dst name: ???  
input dst name > Proxy  
```
Input the name  
(e.g., Squid -> Proxy)
```text
########################################  
file_name:proxy.csv  
########################################  
src ip:192.168.1.3 -> src name: ???  
input src name > Proxy  
dst ip:192.168.1.62 -> dst name: ???  
input dst name > Server  
```
#### 7. Output file is created

1. Created the out.png and out.diag  
2. out.png is the packet sequence file  
3. out.diag is the seqdiag format file  
```bash
$ file out.*
out.diag: ASCII text, with very long lines
out.png:  PNG image data, 1856 x 31706, 8-bit/color RGBA, non-interlaced
```
![output.png](https://raw.githubusercontent.com/wiki/yusukew62/packetseq/images/output.png)
