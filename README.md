# packetseq
Create packet sequence diagram from pcap format csv file

## Description
Create the image file of the packet sequence diagram based on the multiple packet captured files.
Input files uses the csv files made from the pcap files.
Output file is the png file.

## Requirements
* Python 2.7
* setuptools
* seqdiag

## Install
pip install packetseq

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
> Client (Windows 7) --- Proxy (Squid) --- Server (nifty.com)

#### 1. Capture the network packets on the multiple network nodes  

1. Capture the packets using the wireshark on the Windows 7  
(e.g., file name is client.pcap)
2. Capture the packets using the tcpdump on the Proxy Server  
(e.g., file name is proxy.pcap)

#### 2. Export the only communication of specific source port from the capture files using the wireshark  

1. Check the port number to squeeze the specific source port
2. Perform a filter on the wireshark  

> tcp.port == "soure port number"

#### 3. Save as a CSV file

1. Select the following colum on the wireshark

> "No.","Time","Source","Destination","Protocol","Length","Info"  

2. Select the 'Date and Time of Day' in the 'Time Display Format' from menu

> 1973-06-14 01:02:03.123456  

3. Save as a csv file on the wireshark  
(e.g., file name are client.csv, proxy.csv)

#### 4. Send csv files to the environment having the packetseq

#### 5. Run the packetseq

> $ packetseq client.csv proxy.csv

#### 6. Enter the name of the other devices of communication from the standard input  

1. Input the name  
(e.g., Windows 7 -> Client)

> \########################################  
> file_name:client.csv  
> \########################################  
> src ip:192.168.1.3 -> src name: ???  
> input src name > Client  
> dst ip:192.168.1.62 -> dst name: ???  
> input dst name > Proxy  

2. Input the name  
(e.g., Squid -> Proxy)

> \########################################  
> file_name:proxy.csv  
> \########################################  
> src ip:192.168.1.3 -> src name: ???  
> input src name > Proxy  
> dst ip:192.168.1.62 -> dst name: ???  
> input dst name > Server  

#### 7. Output file is created

1. Created the out.png and out.diag  
2. out.png is the packet sequence file  
3. out.diag is the seqdiag format file  

> $ file out.*  
out.diag: ASCII text, with very long lines  
out.png:  PNG image data, 1856 x 31706, 8-bit/color RGBA, non-interlaced  

