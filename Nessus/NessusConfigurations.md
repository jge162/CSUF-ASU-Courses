This document consolidates all the commands and instructions for managing and troubleshooting Nessus, network configurations, and more on Linux and macOS:

---

# Nessus and Network Configuration Commands for Linux and macOS

## 1. **Installing and Managing Nessus on macOS**

### 1.1. **Starting Nessus Manually**
To start Nessus manually on macOS:
```bash
sudo /Library/Nessus/run/sbin/nessusd
```

### 1.2. **Creating a Launch Daemon for Automatic Startup**
To ensure Nessus starts automatically at boot:

1. **Create the Launch Daemon File:**
   ```bash
   sudo nano /Library/LaunchDaemons/com.tenable.nessusd.plist
   ```

2. **Add the Following Content:**
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Label</key>
        <string>com.tenable.nessusd</string>
        <key>ProgramArguments</key>
        <array>
            <string>/Library/Nessus/run/sbin/nessusd</string>
        </array>
        <key>RunAtLoad</key>
        <true/>
        <key>KeepAlive</key>
        <true/>
    </dict>
    </plist>
    ```

3. **Load the Launch Daemon:**
   ```bash
   sudo launchctl load /Library/LaunchDaemons/com.tenable.nessusd.plist
   ```

### 1.3. **Checking Nessus Status**

#### **Check if the Nessus Process is Running:**
```bash
ps aux | grep nessusd
```

#### **Check for Open Ports (Port 8834 for Nessus):**
```bash
sudo lsof -i :8834
```

#### **Verify Launch Daemon Status:**
```bash
sudo launchctl list | grep com.tenable.nessusd
```

## 2. **Managing IP Forwarding and Port Forwarding**

### 2.1. **Checking IP Forwarding Status**

#### **On macOS:**
```bash
sysctl net.inet.ip.forwarding
```

- To disable IP forwarding:
  ```bash
  sudo sysctl -w net.inet.ip.forwarding=0
  ```

- To make the change permanent:
  ```bash
  sudo nano /etc/sysctl.conf
  ```
  Add the line:
  ```bash
  net.inet.ip.forwarding=0
  ```

#### **On Linux:**
```bash
sysctl net.ipv4.ip_forward
```

- Disable IP forwarding:
  ```bash
  sudo sysctl -w net.ipv4.ip_forward=0
  ```

- Make it persistent:
  ```bash
  sudo nano /etc/sysctl.conf
  ```
  Add the line:
  ```bash
  net.ipv4.ip_forward=0
  ```

### 2.2. **Checking for Port Forwarding and Open Ports**

#### **Using `nmap` to Scan for Open Ports:**
```bash
nmap -p- <IP-Address>
```

#### **Checking for Active NAT and Port Forwarding Rules on macOS:**
```bash
sudo pfctl -s nat
```

#### **Checking the Routing Table:**
```bash
netstat -r
```

## 3. **Network and Device Identification**

### 3.1. **Identify Devices on Your Network**

#### **Using `nmap` to Discover Devices:**
```bash
sudo nmap -sn 192.x.x.0/24
```

#### **Check Network Interface MAC Addresses on macOS:**
```bash
ifconfig
```

- Quick check for a specific interface:
  ```bash
  networksetup -getmacaddress en0
  ```

#### **Check ARP Table for MAC Addresses:**
```bash
arp -a
```

### 3.2. **Monitoring Network Traffic**

#### **Using `tcpdump` to Monitor Traffic:**
```bash
sudo tcpdump -i any -n
```

## 4. **Additional Useful Commands**

### 4.1. **Check Disk Space on Linux/macOS:**
```bash
df -h
```

### 4.2. **Review Nessus Logs (Linux Path Example):**
```bash
cd /opt/nessus/var/nessus/logs/
```

---

This document should serve as a comprehensive reference for managing Nessus and checking various network configurations on both Linux and macOS.
