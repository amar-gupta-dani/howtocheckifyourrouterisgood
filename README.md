# How to check if your router tries to protect you

**ARP Spoofing** also known as Man in the Middle is simple but powerful attack. It exploits the vulnerabilites of ARP (Address Resolution Protocol)

-------------------------------------------------------------------------------

## How it Works

Normally these are how the computers in a network communicate (this works for ethernet switches).  

![Load](https://www.google.com/url?sa=i&url=http%3A%2F%2Fwww.shortestpathfirst.net%2F2010%2F11%2F18%2Fman-in-the-middle-mitm-attacks-explained-arp-poisoining%2F95%2F&psig=AOvVaw2_MqN2L0U2eaSzSgOzLver&ust=1610721127856000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCJCnq_rRm-4CFQAAAAAdAAAAABAJ)

The victim (who is not the victim yet) sends an ARP broadcast to ask what are the MAC addresses of the machines with the given IP. For example, the ARP request asks who 192.168.1.1 is, the router has that IP and the router sends its MAC address to the machine that asked. The machine will then update its table so whenever it needs to send something to 192.168.1.1, it will send it to the MAC address that was given. You may now see what the vulnerability is. I could send a message to the victim saying that I'm 192.168.1.1 but give it **MY** MAC address. Now when it needs to send something to 192.168.1.1, it will send the requests to my MAC address. *The **power** feels great!*

![Get rekt](https://miro.medium.com/max/604/1*js1_DvuV5xfA5d6-_vebog.png)
