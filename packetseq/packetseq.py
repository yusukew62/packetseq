# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import csv
import re


class PacketSeq():

    def __init__(self, files):
        self.files = files
        self.syn_list = list()
        self.packet_list = list()
        self.seqdiag_list = list()
        self.color_dict = {"Default":"Blue", "URG":"Red", "ACK":"Green", 
            "PSH":"Red", "RST":"Red", "SYN":"Green", "FIN":"Green"}

    def set_direction(self):
        syn_pattern = re.compile('SYN')

        for in_file in self.files:
            with open(in_file, 'rt') as fin:
                cin = csv.reader(fin)
                for packet in cin:
                    m = syn_pattern.search(str(packet))
                    if m:
                        self.syn_list.append({
                            "file_name": in_file,
                            "src_ip": str(packet[2]),
                            "dst_ip": str(packet[3]),
                        })
                        break

    def set_name(self):
        for syn in self.syn_list:
            print('########################################')
            print('file_name:{}'.format(syn["file_name"]))
            print('########################################')

            print('src ip:{} -> src name: ???'.format(syn["src_ip"]))
            sys.stdout.write('input src name > ')
            syn["src"] = input()

            print('dst ip:{} -> dst name: ???'.format(syn["dst_ip"]))
            sys.stdout.write('input dst name > ')
            syn["dst"] = input()

    def convert_name(self):
        num_pattern = re.compile('No.')

        for in_file in self.syn_list:
            with open(in_file["file_name"], 'rt') as fin:
                cin = csv.reader(fin)
                for packet in cin:
                    conv_src_packet = str(packet).replace(
                        in_file["src_ip"], in_file["src"])

                    conv_packet = conv_src_packet.replace(
                        in_file["dst_ip"], in_file["dst"])

                    packet = conv_packet.split(",")

                    packet_info = ""
                    for info in range(6, len(packet)):
                        packet_info += packet[info]

                    m = num_pattern.search(str(packet))
                    if not m:
                        self.packet_list.append('{},{},{},{}'
                        .format(packet[1], packet[2], packet[3], packet_info))

    def create_diag(self):
        out_file = os.path.exists('out.diag')
        if out_file:
            os.remove('out.diag')

        self.packet_list.sort()
        for i in self.packet_list:
            packet = i.split(",")
            color = ""
            for j in self.color_dict.keys():
                if re.search(str(j),packet[3]):
                    color = self.color_dict[j]
                    break
            else:
                color = self.color_dict["Default"]
            self.seqdiag_list.append('  {} -> {} [ diagonal, label = " {}\n{} ", color = {} ]; '
            .format(packet[1], packet[2], packet[0], packet[3], color))

        with open('out.diag', 'a') as fout:
            fout.write('{}\n'.format('seqdiag {'))
            fout.write('{}\n'.format(' edge_length = 600;'))
            fout.write('{}\n'.format(' span_height = 10;'))
            fout.write('{}\n'.format(' default_fontsize = 20;'))
            fout.write('{}\n'.format(' activation = none;'))
            for i in self.seqdiag_list:
                fout.write('{}\n'.format(i))
            fout.write('{}\n'.format('}'))

    def create_image(self):
        diag_file = "out.diag"
        subprocess.call(["seqdiag", diag_file])


def main():
    packetseq = PacketSeq(sys.argv[1:])
    packetseq.set_direction()
    packetseq.set_name()
    packetseq.convert_name()
    packetseq.create_diag()
    packetseq.create_image()


if __name__ == '__main__':
    main()
