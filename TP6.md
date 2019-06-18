# B1 Réseau 2019 - TP6

## Sommaire
* [Lab 1 : Simple OSPF](#lab-1--simple-ospf)
* [Lab 2 : Un peu de complexité (et d'utilité ?)](#lab-2--un-peu-de-complexité-et-dutilité-)
  * [1. Présentation du lab et contexte](#1-présentation-du-lab-et-contexte)
    * Schéma de la topologie
    * Aires OSPF
    * Réseaux IP et aires OSPF
    * Adressage IP des machines
  * [2. Mise en place du lab](#2-mise-en-place-du-lab)
    * [Adressage statique - routeurs](#checklist-ip-routeurs)
    * [Adressage statique - VMs](#checklist-vms)
    * [OSPF](#vérifier-que-tout-ça-fonctionne)
* [Lab 3 : Let's end this properly](#lab-3--lets-end-this-properly)
  * [NAT (accès internet dans tout le réseau)](#1-nat--accès-internet)
  * [Un service d'infra](#2-un-service-dinfra)
  * [DHCP (adressage dynamique pour les clients)](#3-serveur-dhcp)
  * [DNS](#4-serveur-dns)
  * [NTP (synchronisation de l'heure)](#5-serveur-ntp)
* [Bilan](#bilan)
* [Aller plus loin](#aller-plus-loin)

# Lab 1 : Simple OSPF

Petit lab simple pour comprendre le concept.

# Lab 2 : Un peu de complexité (et d'utilité ?)

## 1. Présentation du lab et contexte

Notre labo aura cette forme; avec une infrastructure de 5 routeurs, 2 clients et 1 serveur)

![maptp6](https://github.com/Genisys33/CCNA/blob/master/Image-Tp2/mapTP6.png)

Nous avons fait nos addressages Ip suivant ce format : 

Machines | `10.6.100.0/30` | `10.6.100.4/30` | `10.6.100.8/30` | `10.6.100.12/30` | `10.6.101.0/30` | `10.6.201.0/24` | `10.6.202.0/24`
--- | --- | --- | --- | --- | --- | --- | --- 
Router1 | `10.6.100.1` | `10.6.100.5` | xXx | xXx | xXx | xXx | `10.6.202.254`
Router2 | `10.6.100.2` | xXx |  `10.6.100.9` | xXx | xXx | xXx | xXx
Router3 | xXx | xXx | `10.6.100.10` | `10.6.100.14` | `10.6.101.1` | xXx | xXx
Router4 | xXx |  `10.6.100.6` | xXx | `10.6.100.13` | xXx | xXx | xXx
Router5 | xXx | xXx | xXx | xXx |  `10.6.101.2` |  `10.6.201.254` | xXx
Client1 | xXx | xXx | xXx | xXx | xXx |  `10.6.201.10` | xXx
Client2 | xXx | xXx | xXx | xXx | xXx |  `10.6.201.11` | xXx
Server | xXx | xXx | xXx | xXx | xXx | xXx | `10.6.202.10`

## 2. Mise en place du lab

### Checklist IP Routeurs

<details><summary>Maintenant nous mêttons en place les adresses ip de nos routeurs et leurs nom de domaine</summary>

Router1 :
 
```bash
  Router1#show ip int br
  Interface                  IP-Address      OK? Method Status                Protocol
  Ethernet0/0                10.6.202.254    YES NVRAM  up                    up      
  Ethernet0/1                10.6.100.1      YES NVRAM  up                    up      
  Ethernet0/2                10.6.100.5      YES NVRAM  up                    up      
  Ethernet0/3                unassigned      YES NVRAM  administratively down down    
  Router1#
```
Router2 :
```bash
  Router2#show ip int br 
  Interface                  IP-Address      OK? Method Status                Protocol
  Ethernet0/0                10.6.100.2      YES NVRAM  up                    up      
  Ethernet0/1                10.6.100.9      YES NVRAM  up                    up      
  Ethernet0/2                unassigned      YES NVRAM  administratively down down    
  Ethernet0/3                unassigned      YES NVRAM  administratively down down    
  Router2#
```

Router3 :
```bash
  Router3#show ip int br
  Interface                  IP-Address      OK? Method Status                Protocol
  Ethernet0/0                10.6.100.10     YES NVRAM  up                    up      
  Ethernet0/1                10.6.100.14     YES NVRAM  up                    up      
  Ethernet0/2                10.6.101.1      YES NVRAM  up                    up      
  Ethernet0/3                unassigned      YES NVRAM  administratively down down    
  Router3#
``` 

Router4 :
```bash
  Router4#show ip int br
  Interface                  IP-Address      OK? Method Status                Protocol
  Ethernet0/0                10.6.100.13     YES NVRAM  up                    up      
  Ethernet0/1                10.6.100.6      YES NVRAM  up                    up      
  Ethernet0/2                unassigned      YES NVRAM  administratively down down    
  Ethernet0/3                unassigned      YES NVRAM  administratively down down    
  Router4#
```

Router5 :
```bash
  Router5#show ip int br 
  Interface                  IP-Address      OK? Method Status                Protocol
  Ethernet0/0                10.6.101.2      YES NVRAM  up                    up      
  Ethernet0/1                10.6.201.254    YES NVRAM  up                    up      
  Ethernet0/2                unassigned      YES NVRAM  administratively down down    
  Ethernet0/3                unassigned      YES NVRAM  administratively down down    
  Router5#
  ```
</details>

### Checklist VMs

<details><summary>Celle des vMs</summary>

Client1 :
```bash
  [root@client1 simon]# ip a && cat /etc/hosts
  2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
      link/ether 08:00:27:91:25:36 brd ff:ff:ff:ff:ff:ff
      inet 10.6.201.10/24 brd 10.6.201.255 scope global noprefixroute enp0s3
         valid_lft forever preferred_lft forever
      inet6 fe80::a00:27ff:fe91:2536/64 scope link 
         valid_lft forever preferred_lft forever
  127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
  ::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
  10.6.201.11 client2
  10.6.202.10 server
  [root@client1 simon]# 
```
Client2 :
```bash
  [root@client2 simon]# ip a && cat /etc/hosts
  2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
      link/ether 08:00:27:21:57:cb brd ff:ff:ff:ff:ff:ff
      inet 10.6.201.11/24 brd 10.6.201.255 scope global noprefixroute enp0s3
         valid_lft forever preferred_lft forever
      inet6 fe80::a00:27ff:fe21:57cb/64 scope link 
         valid_lft forever preferred_lft forever
  127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
  ::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
  10.6.201.10 client1
  10.6.202.10 server
  [root@client2 simon]#
``` 
Server :
  ```bash
   [root@serveur simon]# ip a && cat /etc/hosts
  2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
      link/ether 08:00:27:27:e9:d5 brd ff:ff:ff:ff:ff:ff
      inet 10.6.202.10/24 brd 10.6.202.255 scope global noprefixroute enp0s3
         valid_lft forever preferred_lft forever
      inet6 fe80::a00:27ff:fe27:e9d5/64 scope link 
         valid_lft forever preferred_lft forever
  10.6.201.10 client1
  10.6.201.11 client2
  [root@server simon]#
```

</details>

### Vérifier que tout ça fonctionne

<details><summary>Nous allons maintenant configurer correctement l'ospf qui se chargera de nos routes entre les routeurs.</summary>

Router1 :
```bash
  Router1#show ip route
  Gateway of last resort is not set

       10.0.0.0/8 is variably subnetted, 7 subnets, 2 masks
  O       10.6.100.8/30 [110/20] via 10.6.100.2, 00:18:51, Ethernet0/1
  O       10.6.100.12/30 [110/20] via 10.6.100.6, 00:18:51, Ethernet0/2
  C       10.6.100.0/30 is directly connected, Ethernet0/1
  O IA    10.6.101.0/30 [110/30] via 10.6.100.6, 00:18:51, Ethernet0/2
                        [110/30] via 10.6.100.2, 00:18:51, Ethernet0/1
  C       10.6.100.4/30 is directly connected, Ethernet0/2
  O IA    10.6.201.0/24 [110/40] via 10.6.100.6, 00:18:45, Ethernet0/2
                        [110/40] via 10.6.100.2, 00:18:46, Ethernet0/1
  C       10.6.202.0/24 is directly connected, Ethernet0/0
  Router1#show ip protocols                                          
  Routing Protocol is "ospf 1"
    Outgoing update filter list for all interfaces is not set
    Incoming update filter list for all interfaces is not set
    Router ID 1.1.1.1
    It is an area border router
    Number of areas in this router is 2. 2 normal 0 stub 0 nssa
    Maximum path: 4
    Routing for Networks:
      10.6.100.0 0.0.0.3 area 0
      10.6.100.4 0.0.0.3 area 0
      10.6.202.0 0.0.0.255 area 2
   Reference bandwidth unit is 100 mbps
    Routing Information Sources:
      Gateway         Distance      Last Update
      4.4.4.4              110      00:21:32
      3.3.3.3              110      00:21:26
    Distance: (default is 110)

  Router1#show ip ospf neighbor

  Neighbor ID     Pri   State           Dead Time   Address         Interface
  4.4.4.4           1   FULL/DR         00:00:33    10.6.100.6      Ethernet0/2
  2.2.2.2           1   FULL/DR         00:00:33    10.6.100.2      Ethernet0/1
  Router1#
``` 
Router2 :
```bash
  Router2#show ip route
  Gateway of last resort is not set

       10.0.0.0/8 is variably subnetted, 7 subnets, 2 masks
  C       10.6.100.8/30 is directly connected, Ethernet0/1
  O       10.6.100.12/30 [110/20] via 10.6.100.10, 00:23:12, Ethernet0/1
  C       10.6.100.0/30 is directly connected, Ethernet0/0
  O IA    10.6.101.0/30 [110/20] via 10.6.100.10, 00:23:12, Ethernet0/1
  O       10.6.100.4/30 [110/20] via 10.6.100.1, 00:23:12, Ethernet0/0
  O IA    10.6.201.0/24 [110/30] via 10.6.100.10, 00:23:12, Ethernet0/1
  O IA    10.6.202.0/24 [110/20] via 10.6.100.1, 00:23:14, Ethernet0/0
  Router2#show ip protocols
  Routing Protocol is "ospf 1"
    Outgoing update filter list for all interfaces is not set
    Incoming update filter list for all interfaces is not set
    Router ID 2.2.2.2
    Number of areas in this router is 1. 1 normal 0 stub 0 nssa
    Maximum path: 4
    Routing for Networks:
      10.6.100.0 0.0.0.3 area 0
      10.6.100.8 0.0.0.3 area 0
   Reference bandwidth unit is 100 mbps
    Routing Information Sources:
      Gateway         Distance      Last Update
      1.1.1.1              110      00:23:17
      4.4.4.4              110      00:23:17
      3.3.3.3              110      00:23:17
    Distance: (default is 110)

  Router2#show ip ospf neighbor

  Neighbor ID     Pri   State           Dead Time   Address         Interface
  3.3.3.3           1   FULL/DR         00:00:38    10.6.100.10     Ethernet0/1
  1.1.1.1           1   FULL/BDR        00:00:38    10.6.100.1      Ethernet0/0
  Router2#
```
Router3 :
```bash
  Router3#show ip route
  Gateway of last resort is not set

       10.0.0.0/8 is variably subnetted, 7 subnets, 2 masks
  C       10.6.100.8/30 is directly connected, Ethernet0/0
  C       10.6.100.12/30 is directly connected, Ethernet0/1
  O       10.6.100.0/30 [110/20] via 10.6.100.9, 00:25:16, Ethernet0/0
  C       10.6.101.0/30 is directly connected, Ethernet0/2
  O       10.6.100.4/30 [110/20] via 10.6.100.13, 00:25:16, Ethernet0/1
  O       10.6.201.0/24 [110/20] via 10.6.101.2, 00:25:16, Ethernet0/2
  O IA    10.6.202.0/24 [110/30] via 10.6.100.13, 00:25:16, Ethernet0/1
                        [110/30] via 10.6.100.9, 00:25:17, Ethernet0/0
  Router3#show ip protocols
  Routing Protocol is "ospf 1"
    Outgoing update filter list for all interfaces is not set
    Incoming update filter list for all interfaces is not set
    Router ID 3.3.3.3
    It is an area border router
    Number of areas in this router is 2. 2 normal 0 stub 0 nssa
    Maximum path: 4
    Routing for Networks:
      10.6.100.8 0.0.0.3 area 0
      10.6.100.12 0.0.0.3 area 0
      10.6.101.0 0.0.0.3 area 1
   Reference bandwidth unit is 100 mbps
    Routing Information Sources:
      Gateway         Distance      Last Update
      1.1.1.1              110      00:25:21
      4.4.4.4              110      00:25:21
      5.5.5.5              110      00:25:21
      2.2.2.2              110      00:25:21
    Distance: (default is 110)

  Router3#show ip ospf neighbor

  Neighbor ID     Pri   State           Dead Time   Address         Interface
  4.4.4.4           1   FULL/DR         00:00:30    10.6.100.13     Ethernet0/1
  2.2.2.2           1   FULL/BDR        00:00:31    10.6.100.9      Ethernet0/0
  5.5.5.5           1   FULL/DR         00:00:31    10.6.101.2      Ethernet0/2
  Router3#
```
Router4 :
```bash
  Router4#show ip route
  Gateway of last resort is not set
       10.0.0.0/8 is variably subnetted, 7 subnets, 2 masks
  O       10.6.100.8/30 [110/20] via 10.6.100.14, 00:26:33, Ethernet0/0
  C       10.6.100.12/30 is directly connected, Ethernet0/0
  O       10.6.100.0/30 [110/20] via 10.6.100.5, 00:26:33, Ethernet0/1
  O IA    10.6.101.0/30 [110/20] via 10.6.100.14, 00:26:33, Ethernet0/0
  C       10.6.100.4/30 is directly connected, Ethernet0/1
  O IA    10.6.201.0/24 [110/30] via 10.6.100.14, 00:26:28, Ethernet0/0
  O IA    10.6.202.0/24 [110/20] via 10.6.100.5, 00:26:34, Ethernet0/1
  Router4#show ip route
  Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP
         D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
         N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
         E1 - OSPF external type 1, E2 - OSPF external type 2
         i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
         ia - IS-IS inter area, * - candidate default, U - per-user static route
         o - ODR, P - periodic downloaded static route

  Gateway of last resort is not set

       10.0.0.0/8 is variably subnetted, 7 subnets, 2 masks
  O       10.6.100.8/30 [110/20] via 10.6.100.14, 00:26:37, Ethernet0/0
  C       10.6.100.12/30 is directly connected, Ethernet0/0
  O       10.6.100.0/30 [110/20] via 10.6.100.5, 00:26:37, Ethernet0/1
  O IA    10.6.101.0/30 [110/20] via 10.6.100.14, 00:26:37, Ethernet0/0
  C       10.6.100.4/30 is directly connected, Ethernet0/1
  O IA    10.6.201.0/24 [110/30] via 10.6.100.14, 00:26:31, Ethernet0/0
  O IA    10.6.202.0/24 [110/20] via 10.6.100.5, 00:26:38, Ethernet0/1
  Router4#show ip ospf neighbor

  Neighbor ID     Pri   State           Dead Time   Address         Interface
  3.3.3.3           1   FULL/BDR        00:00:39    10.6.100.14     Ethernet0/0
  1.1.1.1           1   FULL/BDR        00:00:39    10.6.100.5      Ethernet0/1
  Router4#
```

Router5 :
```bash
  Router5#show ip route
  Gateway of last resort is not set

       10.0.0.0/8 is variably subnetted, 7 subnets, 2 masks
  O IA    10.6.100.8/30 [110/20] via 10.6.101.1, 00:28:01, Ethernet0/0
  O IA    10.6.100.12/30 [110/20] via 10.6.101.1, 00:28:01, Ethernet0/0
  O IA    10.6.100.0/30 [110/30] via 10.6.101.1, 00:28:01, Ethernet0/0
  C       10.6.101.0/30 is directly connected, Ethernet0/0
  O IA    10.6.100.4/30 [110/30] via 10.6.101.1, 00:27:56, Ethernet0/0
  C       10.6.201.0/24 is directly connected, Ethernet0/1
  O IA    10.6.202.0/24 [110/40] via 10.6.101.1, 00:27:56, Ethernet0/0
  Router5#show ip protocols
  Routing Protocol is "ospf 1"
    Outgoing update filter list for all interfaces is not set
    Incoming update filter list for all interfaces is not set
    Router ID 5.5.5.5
    Number of areas in this router is 1. 1 normal 0 stub 0 nssa
    Maximum path: 4
    Routing for Networks:
      10.6.101.0 0.0.0.3 area 1
      10.6.201.0 0.0.0.255 area 1
   Reference bandwidth unit is 100 mbps
    Routing Information Sources:
      Gateway         Distance      Last Update
      3.3.3.3              110      00:28:02
    Distance: (default is 110)
  Router5#show ip ospf neighbor

  Neighbor ID     Pri   State           Dead Time   Address         Interface
  3.3.3.3           1   FULL/BDR        00:00:35    10.6.101.1      Ethernet0/0
  Router5#
```
</details>

<details><summary>Nous allons ping le server avec les clients et l'inverse, si les routes ont correctements définis tout devrait fonctionner.</summary>

Router1 :
```bash
[root@client1 simon]# ping -c 4 server
PING server (10.6.202.10) 56(84) bytes of data.
64 bytes from server (10.6.202.10): icmp_seq=2 ttl=60 time=53.6 ms
64 bytes from server (10.6.202.10): icmp_seq=3 ttl=60 time=59.0 ms
64 bytes from server (10.6.202.10): icmp_seq=4 ttl=60 time=48.1 ms

--- server ping statistics ---
4 packets transmitted, 3 received, 25% packet loss, time 3007ms
rtt min/avg/max/mdev = 48.175/53.603/59.030/4.431 ms
[root@client1 simon]# 
```

Router2 :
```bash
root@client2 simon]# ping -c 4 server 
PING server (10.6.202.10) 56(84) bytes of data.
64 bytes from server (10.6.202.10): icmp_seq=1 ttl=60 time=56.5 ms
64 bytes from server (10.6.202.10): icmp_seq=2 ttl=60 time=49.9 ms
64 bytes from server (10.6.202.10): icmp_seq=3 ttl=60 time=47.5 ms
64 bytes from server (10.6.202.10): icmp_seq=4 ttl=60 time=41.9 ms

--- server ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3011ms
rtt min/avg/max/mdev = 41.941/48.990/56.581/5.255 ms
[root@client2 simon]# 
```

Server :
```bash
  [root@serveur simon]# ping -c 4 client1 && ping -c 4 client2
  PING client1 (10.6.201.10) 56(84) bytes of data.
  64 bytes from client1 (10.6.201.10): icmp_seq=1 ttl=60 time=48.8 ms
  64 bytes from client1 (10.6.201.10): icmp_seq=2 ttl=60 time=46.0 ms
  64 bytes from client1 (10.6.201.10): icmp_seq=3 ttl=60 time=43.0 ms
  64 bytes from client1 (10.6.201.10): icmp_seq=4 ttl=60 time=61.3 ms

  --- client1 ping statistics ---
  4 packets transmitted, 4 received, 0% packet loss, time 3003ms
  rtt min/avg/max/mdev = 43.084/49.829/61.358/6.961 ms
  PING client2 (10.6.201.11) 56(84) bytes of data.
  64 bytes from client2 (10.6.201.11): icmp_seq=1 ttl=60 time=45.9 ms
  64 bytes from client2 (10.6.201.11): icmp_seq=2 ttl=60 time=44.8 ms
  64 bytes from client2 (10.6.201.11): icmp_seq=3 ttl=60 time=61.2 ms
  64 bytes from client2 (10.6.201.11): icmp_seq=4 ttl=60 time=57.8 ms

  --- client2 ping statistics ---
  4 packets transmitted, 4 received, 0% packet loss, time 3003ms
  rtt min/avg/max/mdev = 44.851/52.492/61.233/7.181 ms
  [root@serveur simon]#
```
Parfait le Labo est bien en place.

</details>

# Lab 3 : Let's end this properly

## 1. NAT : accès internet

<details><summary>Nous allons configurer notre NAt qui nous servira à connecter nos VMs à internet.</summary>

```bash
Router4#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
Router4(config)#interface ethernet 0/2
Router4(config-if)#ip address dhcp
Router4(config-if)#no shut
Router4(config-if)#end
Router4#show ip int br
Interface                  IP-Address      OK? Method Status                Procol
Ethernet0/0                10.6.100.13     YES NVRAM  up                    up
Ethernet0/1                10.6.100.6      YES NVRAM  up                    up
Ethernet0/2                192.168.122.181 YES DHCP   up                    up
Ethernet0/3                unassigned      YES NVRAM  administratively down do
Router4#ping 8.8.8.8
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 36/41/52 ms
Router4(config)#interface ethernet 0/2
Router4(config-if)#ip nat outside
*Mar  1 00:43:46.295: %LINEPROTO-5-UPDOWN: Line protocol on Interface NVI0, changed state to up
Router4(config-if)#exit
Router4(config)#interface ethernet 0/1
Router4(config-if)#ip nat inside
Router4(config-if)#exit
Router4(config)#interface ethernet 0/0
Router4(config-if)#ip nat inside
Router4(config-if)#exit
Router4(config)#
Router4(config)#ip nat inside source list 1 interface ethernet 0/2 overload
Router4(config)#access-list 1 permit any
Router4(config)#router ospf 1
Router4(config-router)#default-information originate
```
Et voici si tout est bien configuré toute les machines peuvent faire `ping 8.8.8.8`, nous allons donc vérifier ça :

```bash
Router1#ping 8.8.8.8
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 44/127/188 ms
Router2#ping 8.8.8.8
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 64/82/148 ms
Router3#ping 8.8.8.8
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 40/53/76 ms
Router4#ping 8.8.8.8
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 28/44/64 ms
Router5#ping 8.8.8.8
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 52/71/88 ms
```

Tout est bien configuré, chaque machine est bien configurée, bien évidement il ne faut pas oublié de faire un petit `wr`pour nous sauvez d'un seconde reconfiguration.

</details>

## 2. Un service d'infra

<details><summary>Nous allons mêttres en place notre petit serveur sur notre Vms server avec un outil que l'on connais bien qui est `Nginx`</summary>
 
 Après pas mal de galère et un refus de notre ssh j'ai du passer par le serveur Python utilisé dans les tps précédents :
 
 ```bash
[root@client1 simon]# curl server
 <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <title>Test Page for the Nginx HTTP Server on Fedora</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <style type="text/css">
            /*<![CDATA[*/
            body {
                background-color: #fff;
                color: #000;
                font-size: 0.9em;
                font-family: sans-serif,helvetica;
                margin: 0;
                padding: 0;
            }
            :link {
                color: #c00;
            }
            :visited {
                color: #c00;
            }
            a:hover {
                color: #f50;
            }
            h1 {
                text-align: center;
                margin: 0;
                padding: 0.6em 2em 0.4em;
                background-color: #294172;
                color: #fff;
                font-weight: normal;
                font-size: 1.75em;
                border-bottom: 2px solid #000;
            }
            h1 strong {
                font-weight: bold;
                font-size: 1.5em;
            }
            h2 {
                text-align: center;
                background-color: #3C6EB4;
                font-size: 1.1em;
                font-weight: bold;
                color: #fff;
                margin: 0;
                padding: 0.5em;
                border-bottom: 2px solid #294172;
            }
            hr {
                display: none;
            }
            .content {
                padding: 1em 5em;
            }
            .alert {
                border: 2px solid #000;
            }

            img {
                border: 2px solid #fff;
                padding: 2px;
                margin: 2px;
            }
            a:hover img {
                border: 2px solid #294172;
            }
            .logos {
                margin: 1em;
                text-align: center;
            }
            /*]]>*/
        </style>
    </head>

    <body>
        <h1>Welcome to <strong>nginx</strong> on Fedora!</h1>

        <div class="content">
            <p>This page is used to test the proper operation of the
            <strong>nginx</strong> HTTP server after it has been
            installed. If you can read this page, it means that the
            web server installed at this site is working
            properly.</p>

            <div class="alert">
                <h2>Website Administrator</h2>
                <div class="content">
                    <p>This is the default <tt>index.html</tt> page that
                    is distributed with <strong>nginx</strong> on
                    Fedora.  It is located in
                    <tt>/usr/share/nginx/html</tt>.</p>

                    <p>You should now put your content in a location of
                    your choice and edit the <tt>root</tt> configuration
                    directive in the <strong>nginx</strong>
                    configuration file
                    <tt>/etc/nginx/nginx.conf</tt>.</p>

                </div>
            </div>

            <div class="logos">
                <a href="http://nginx.net/"><img
                    src="nginx-logo.png" 
                    alt="[ Powered by nginx ]"
                    width="121" height="32" /></a>

                <a href="http://fedoraproject.org/"><img 
                    src="poweredby.png" 
                    alt="[ Powered by Fedora ]" 
                    width="88" height="31" /></a>
            </div>
        </div>
    </body>
</html>
```
 </details>

## 3. Serveur DHCP

<details><summary>Tout d'abords nous allons faire en sorte de configurer notre client2 en dhcp</summary>
Après l'avoir rennomé nous devons faire `yum install dhcp -y` sur notre vm nous allons mêttre ce fichier dans le répertoire `/etc/dhcp/`

```bash
# dhcpd.conf

# option definitions common to all supported networks
option domain-name "dhcp.b1";

default-lease-time 600;
max-lease-time 7200;

# If this DHCP server is the official DHCP server for the local
# network, the authoritative directive should be uncommented.
authoritative;

# Use this to send dhcp log messages to a different log file (you also
# have to hack syslog.conf to complete the redirection).
log-facility local7;

subnet 10.6.201.0 netmask 255.255.255.0 {
  range 10.6.201.50 10.6.201.100;
  option domain-name "dhcp.b1";
  option routers 10.6.201.254;
  option broadcast-address 10.6.201.255;
}
```
Maintenant nous allons faire un test avec le client 1 pour voir si il fonctionne correctement, la range est de 10.6.201.50 à 10.6.201.100 au niveau des addresses disponble, nous faison donc la commande `dhclient` lient1 :

```bash
[root@client1 simon]# dhclient
[root@client1 simon]# ip a
  2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
      link/ether 08:00:27:e4:02:8d brd ff:ff:ff:ff:ff:ff
      inet 10.6.201.10/24 brd 10.6.201.255 scope global noprefixroute enp0s3
         valid_lft forever preferred_lft forever 
      inet 10.6.201.50/24 brd 10.6.201.255 scope global secondary dynamic enp0s3
         valid_lft 414sec preferred_lft 414sec
      inet6 fe80::fde8:9754:6e03:deae/64 scope link noprefixroute 
         valid_lft forever preferred_lft forever
```
Parfait c'est dans la range 
</details>

## 4. Serveur DNS

<details><summary>Après la mise en place du serveur nous devrons avoir ce résultat</summary>
 
 ```bash
[root@server simon]#dig server1.tp6.b1
; <<>> DiG 9.9.4-RedHat-9.9.4-73.el7_6 <<>> server1.tp6.b1
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 57440
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 1
;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;server1.tp6.b1.			IN	A
;; ANSWER SECTION:
server1.tp6.b1.		604800	IN	A	10.6.202.10
;; AUTHORITY SECTION:
tp6.b1.			604800	IN	NS	server1.tp6.b1.
;; Query time: 0 msec
;; SERVER: 10.6.202.10#53(10.6.202.10)
;; WHEN: Sun Mar 17 22:35:43 CET 2019
;; MSG SIZE  rcvd: 73

[root@server simon]#dig client2.tp6.b1
; <<>> DiG 9.9.4-RedHat-9.9.4-73.el7_6 <<>> client2.tp6.b1
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 22924
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 2
;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;client2.tp6.b1.			IN	A
;; ANSWER SECTION:
client2.tp6.b1.		604800	IN	A	10.6.201.11
;; AUTHORITY SECTION:
tp6.b1.			604800	IN	NS	server1.tp6.b1.
;; ADDITIONAL SECTION:
server1.tp6.b1.		604800	IN	A	10.6.202.10
;; Query time: 0 msec
;; SERVER: 10.6.202.10#53(10.6.202.10)
;; WHEN: Sun Mar 17 22:06:38 CET 2019
;; MSG SIZE  rcvd: 97

[root@server simon]#dig -x 10.6.201.10
; <<>> DiG 9.9.4-RedHat-9.9.4-73.el7_6 <<>> -x 10.6.201.10
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 23040
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 2
;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;10.201.6.10.in-addr.arpa.	IN	PTR
;; ANSWER SECTION:
10.201.6.10.in-addr.arpa. 86400	IN	PTR	client1.tp6.b1.
;; AUTHORITY SECTION:
6.10.in-addr.arpa.	86400	IN	NS	server1.tp6.b1.
;; ADDITIONAL SECTION:
server1.tp6.b1.		604800	IN	A	10.6.202.10
;; Query time: 0 msec
;; SERVER: 10.6.202.10#53(10.6.202.10)
;; WHEN: Sun Mar 17 22:32:51 CET 2019
;; MSG SIZE  rcvd: 119

[root@server simon]#ping client2.tp6.b1
 PING client2.tp6.b1 (10.6.201.11) 56(84) bytes of data.
64 bytes from client2.tp6.b1 (10.6.201.11): icmp_seq=1 ttl=60 time=80.7 ms
64 bytes from client2.tp6.b1 (10.6.201.11): icmp_seq=2 ttl=60 time=77.5 ms
64 bytes from client2.tp6.b1 (10.6.201.11): icmp_seq=3 ttl=60 time=82.3 ms
64 bytes from client2.tp6.b1 (10.6.201.11): icmp_seq=4 ttl=60 time=78.6 ms
--- client2.tp6.b1 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3007ms
rtt min/avg/max/mdev = 77.501/79.809/82.356/1.916 ms
 ```
 
 </details>

## 5. Serveur NTP

```bash
[root@server simon]#cat /etc/chrony.conf
# Servers to synchronize with
# Replace XXX with needed server names
server 0.europe.pool.ntp.org
server 1.europe.pool.ntp.org
server 2.europe.pool.ntp.org
server 3.europe.pool.ntp.org
# Record the rate at which the system clock gains/losses time.
driftfile /var/lib/chrony/drift
# Allow the system clock to be stepped in the first three updates
# if its offset is larger than 1 second.
makestep 1.0 3
# Enable kernel synchronization of the real-time clock (RTC).
rtcsync
# Allow NTP client access from local network.
allow all
# Serve time even if not synchronized to a time source.
local stratum 10
# Specify file containing keys for NTP authentication.
keyfile /etc/chrony.keys
# Specify directory for log files.
logdir /var/log/chrony
# Select which information is logged.
log measurements statistics tracking

[root@server simon]#systemctl status chronyd.service
● chronyd.service - NTP client/server
   Loaded: loaded (/usr/lib/systemd/system/chronyd.service; enabled; vendor preset: enabled)
   Active: active (running) since Sun 2019-03-17 23:25:52 CET; 38min ago
     Docs: man:chronyd(8)
           man:chrony.conf(5)
  Process: 4890 ExecStartPost=/usr/libexec/chrony-helper update-daemon (code=exited, status=0/SUCCESS)
  Process: 4886 ExecStart=/usr/sbin/chronyd $OPTIONS (code=exited, status=0/SUCCESS)
 Main PID: 4888 (chronyd)
   CGroup: /system.slice/chronyd.service
           └─4888 /usr/sbin/chronyd
Mar 17 23:25:52 serveur systemd[1]: Starting NTP client/server...
Mar 17 23:25:52 serveur chronyd[4888]: chronyd version 3.2 starting (+CMDMON +NTP +REFCLOCK +RTC +PRIVDROP +SCFILTER +SECHASH +SIGND +ASYNCDNS +IPV6 +DEBUG)
Mar 17 23:25:52 serveur chronyd[4888]: Frequency -24.281 +/- 201.962 ppm read from /var/lib/chrony/drift
Mar 17 23:25:52 serveur systemd[1]: Started NTP client/server.
Mar 17 23:28:05 serveur chronyd[4888]: Selected source 91.217.155.60
Mar 17 23:29:09 serveur chronyd[4888]: Selected source 200.160.7.193
Mar 17 23:29:10 serveur chronyd[4888]: Source 91.217.155.60 replaced with 51.174.131.248
Mar 17 23:37:49 serveur chronyd[4888]: Selected source 51.174.131.248
```
```

Après avoir configuré nos `chrony.conf`dans chaque vms client nous allons check l'état de la synchronisation NTP :

Sur le serveur :

```bash
[root@server simon]#chronyc sources
210 Number of sources = 3
MS Name/IP address         Stratum Poll Reach LastRx Last sample               
===============================================================================
^- 248.51-174-131.customer.>     1   6    37    49    -23ms[  -23ms] +/-  176ms
^- ntp3.ntp.net.nz               1   6   377   115    +17ms[  +17ms] +/-  186ms
^* gps.ntp.br                    2   6   377    53  +1272us[+1539us] +/-  132ms

[root@server simon]#chronyc tracking
Reference ID    : C8A007C1 (gps.ntp.br)
Stratum         : 3
Ref time (UTC)  : Sun Mar 17 22:34:33 2019
System time     : 0.000250357 seconds fast of NTP time
Last offset     : +0.000266638 seconds
RMS offset      : 0.004327788 seconds
Frequency       : 3.566 ppm fast
Residual freq   : +0.368 ppm
Skew            : 62.041 ppm
Root delay      : 0.258822054 seconds
Root dispersion : 0.005483823 seconds
Update interval : 64.6 seconds
Leap status     : Normal

Sur le Client1 :
```bash
[root@client1 simon]#chronyc tracking
Reference ID    : C1043A2C (cronos.isnic.is)
Stratum         : 3
Ref time (UTC)  : Sun Mar 17 23:16:03 2019
System time     : 0.006442192 seconds fast of NTP time
Last offset     : +0.005730533 seconds
RMS offset      : 0.015224669 seconds
Frequency       : 6.666 ppm slow
Residual freq   : +1.808 ppm
Skew            : 73.906 ppm
Root delay      : 0.120758921 seconds
Root dispersion : 0.010520675 seconds
Update interval : 64.2 seconds
Leap status     : Normal

[root@client1 simon]#chronyc sources
210 Number of sources = 4
MS Name/IP address         Stratum Poll Reach LastRx Last sample               
===============================================================================
^- time100.stupi.se              1   6   377    31    +39ms[  +39ms] +/-   98ms
^- server1.websters-compute>     2   6   377    35   +719us[+6435us] +/-   65ms
^+ scott.red.uv.es               2   6   377    31    +54ms[  +54ms] +/-  139ms
^* cronos.isnic.is               2   6   377    33    +33ms[  +39ms] +/-   91ms
```

# Bilan

Un petit résumé de notre tp : 
Nous avons vu ici à l'aide d'une simulation avec deux clients comment l'ip, la passerelle serveur DNS sont automatiquement configurés grâce au serveur DHCP, et ainsi ils pouvaient joindre internet sans pb ou le serveur NGinx qui était installé en interne. Tout ceci était pour les clients. Au niveau des serveurs nous avons qu'ils sont en charge de la résolution du nom local avec le serveur DNS et les services fournit grâce au serveur web qui était pour nous Nginx. Et pour finir les routeurs qui servaient à mettre en place un routage dynamique (ospf) et ainsi que l'accès Wan grâce au nat. 

Linux_is_better
