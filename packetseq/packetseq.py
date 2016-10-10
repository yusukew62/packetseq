# -*- coding: utf-8 -*-
import argparse
import csv
import os
import re
import subprocess
import sys


class PacketSeq():

    def __init__(self):
        self.files = list()
        self.type = ""
        self.out = ""
        self.syn_list = list()
        self.packet_list = list()
        self.seqdiag_list = list()
        self.color_dict = {
            'SYN': "blue", 'SYN ACK': "red",
            'ACK': "green",
            'FIN': "navy", 'FIN ACK': "maroon",
            'RST': "purple", 'RST ACK': "fuchsia",
            'URG': "olive", 'PSH': "orange",
            'Other': "gray",
        }
        self.info = ""

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

    def set_node_name(self):
        for syn in self.syn_list:
            print('########################################')
            print('file_name:{}'.format(syn["file_name"]))
            print('########################################')

            print('src ip:{} -> src name: ???'.format(syn["src_ip"]))
            sys.stdout.write('input src name > ')
            syn["src"] = raw_input()

            print('dst ip:{} -> dst name: ???'.format(syn["dst_ip"]))
            sys.stdout.write('input dst name > ')
            syn["dst"] = raw_input()
            print('')

    def convert_node_name(self):
        num_pattern = re.compile('No.')

        for in_file in self.syn_list:
            with open(in_file["file_name"], 'rt') as fin:
                cin = csv.reader(fin)
                for p in cin:
                    line = ""
                    for l in p:
                        line += (str(l) + ",")

                    conv_src_packet = str(line).replace(
                        in_file["src_ip"], in_file["src"])

                    conv_packet = conv_src_packet.replace(
                        in_file["dst_ip"], in_file["dst"])

                    packet = conv_packet.split(",")

                    packet_info = ""
                    for info in range(6, len(packet)):
                        packet_info += packet[info]

                    if self.info == "summary":
                        packet_info = re.sub('.*\[', '[', packet_info)
                        packet_info = re.sub('\].*', ']', packet_info)
                    elif self.info == "info":
                        pass
                    elif self.info == "default":
                        packet_info = re.sub('.*\[', '[', packet_info)
                    else:
                        packet_info = re.sub('.*\[', '[', packet_info)

                    m = num_pattern.search(str(packet))
                    if not m:
                        self.packet_list.append('{},{},{},{}'
                                                .format(packet[1], packet[2], packet[3], packet_info))

    def create_diag_file(self):
        out_file = os.path.exists(str(self.out) + '.diag')
        if out_file:
            os.remove(str(self.out) + '.diag')

        self.packet_list.sort()
        for p in self.packet_list:
            packet = p.split(",")
            color = ""
            for color_key in self.color_dict.keys():
                color_match = '\[' + color_key + '\]'
                finditer = re.findall(color_match, packet[3])
                if re.search(color_match, packet[3]):
                    color = self.color_dict[color_key]
                    break
            else:
                color = self.color_dict["Other"]

            self.seqdiag_list.append('  {} -> {} [ diagonal, label = " {}\n{} ", color = {} ]; '
                                     .format(packet[1], packet[2], packet[0], packet[3], color))

        with open(str(self.out) + '.diag', 'a') as fout:
            fout.write('{}\n'.format('seqdiag {'))
            fout.write('{}\n'.format(' edge_length = 600;'))
            fout.write('{}\n'.format(' span_height = 10;'))
            fout.write('{}\n'.format(' default_fontsize = 20;'))
            fout.write('{}\n'.format(' activation = none;'))
            for i in self.seqdiag_list:
                fout.write('{}\n'.format(i))
            fout.write('{}\n'.format('}'))

    def create_sequence_image(self):
        diag_file = str(self.out) + '.diag'
        if self.type == "png":
            subprocess.call(['seqdiag', diag_file])
        elif self.type == "svg":
            subprocess.call(['seqdiag', '-Tsvg', diag_file])

    def set_parser(self):
        parser = argparse.ArgumentParser(version='0.1.5', description="This script to make PNG image \
            file of networking sequence diagram using csv file was made by pcap file.")
        parser.add_argument('files', metavar="file", nargs="+")
        parser.add_argument('-o', '--out', metavar="out", nargs=1, default=['out'],
                            help="decide output file name")
        parser.add_argument('-i', '--info', metavar="info", choices=['summary', 'default', 'info'],
                            nargs=1, default=['default'], help="choose 'summary', 'default' or 'info'")
        parser.add_argument('-t', '--type', metavar="type", choices=['png', 'svg'],
                            nargs=1, default=['png'], help="choose 'png' or 'svg' output file format")
        args = parser.parse_args()
        self.files = args.files
        self.type = args.type[0]
        self.out = args.out[0]
        self.info = args.info[0]


def main():
    packetseq = PacketSeq()
    packetseq.set_parser()
    packetseq.set_direction()
    packetseq.set_node_name()
    packetseq.convert_node_name()
    packetseq.create_diag_file()
    packetseq.create_sequence_image()


if __name__ == '__main__':
    main()
