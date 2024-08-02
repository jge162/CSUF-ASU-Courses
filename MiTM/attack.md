## Challenge Overview

**Level 13 - MiTM ARPing**

This challenge requires you to execute a sophisticated Man-in-the-Middle (MiTM) attack by injecting a TCP packet into network communications between two hosts, `10.0.0.3` and `10.0.0.4`.

## Objectives

- **Reverse Engineer the Protocol:** Analyze and reverse engineer the communication protocol between the two hosts on port `31337`.
- **Inject TCP Packet:** Accurately inject a TCP packet containing the appropriate command into the ongoing communication.

## Technical Approach

- **Scapy for Packet Manipulation:** Utilize Scapy’s `sniff` function with a packet callback filter to identify the precise timing for packet injection.
- **TCP Communication Analysis:** Monitor both sides of the communication using `tcpdump`, and leave out the `dst` parameter of the `Ether` frame layer to capture all relevant packets.
- **ARP Spoofing:** Implement ARP spoofing to position yourself as the intermediary in the communication flow.

## Getting Started

1. **Launch the Challenge:** Begin by running `/challenge/run`.
2. **MAC Address Identification:** The MAC addresses of the client and server will be displayed at the start. Use this information to facilitate your packet injection strategy.
