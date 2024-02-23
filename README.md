# Xiaochen's Home Router

This document describes my requirements for the home router, and why. And all the configurations and scripts will be in the repo.

## Goals
1. The router should be able to connect to the Internet via a WAN port, and support global VPN connecting through the router.

1. The router should have a good performance, reasonable storage, and run a OpenWrt Distribution.

    1. I have many requirements for the router. Also, the #1 consumes many resources, so I need a router with good performance.
      
    1. I am enough of the 64MB flash and 512MB RAM. Hey, Router manufacturers. Listen, it is 2023, NOT 2003. Can't you add more memory and flash? The cost of memory and flash storage is very very low now. Anyway, I will have a 64GB m-sata SSD, and 4GB RAM.

    1. OpenWrt gives me the power to customize the router. I can install any packages I want.

1. Router will expose the wanted web server to the Internet.
1. DDNS support
1. Wireguard VPN server to connect to the home network
1. Small dependence on OpenWrt Version

    I may use different OpenWrt versions to test and run at initial time, also I may upgrade the version in the future, so I want to make the configurations as independent as possible.

## No Goals
1. No WiFi support
    
    WiFi will be handled by home WiFi APs. So that I can have a better WiFi coverage using the Mesh WiFi. Also, I do not need to upgrade the router when I want to upgrade the WiFi.
    
    The router can have many configurations, but the WiFi APs are not. Also, WiFi-7 is coming. I do not want my router to be outdated when WiFi-7 is coming.

1. No complicated services like NAS, media server, etc.

    I will have a dedicated NAS server, and a dedicated media server. I want my router to be a router, not a server. My network experience is the most important thing. I do not want my server be slow down when other services are running. Put all the eggs in one basket is not a good idea.

## Hardware

A mini PC with 4 network ports.

| Item    | Description               | Note                                                                                      |
|---------|---------------------------|-------------------------------------------------------------------------------------------|
| CPU     | Intel Celeron N4100       | 4 cores, 4 threads, 6w TDP.<br> it is enough for a 2.5Gbps network and a VPN under 1Gbps. |
| RAM     | 4GB                       | 1 of 2 memory slot is used, a future upgrade is possible                                  |
| Storage | 64GB m-sata SSD           |                                                                                           |
| Network | 4x 2.5Gbps Ethernet ports | 2.5Gbps for future                                                                        |
| WiFi    | No                        |                                                                                           |

## Software

### OS
OpenWrt

### Docker
I will use [Docker on OpenWrt](https://openwrt.org/docs/guide-user/virtualization/docker_host) to run some services. Some services will require complex configurations, and a long compile chain, and they may break OpenWrt's own packages. So I will use Docker to run them.

### Nginx
Nginx is used for expose websites to the Internet. I will use it to expose my services to the Internet. OpenWrt's own web server is uhttpd, but it is for the router's own web UI. I do not want to make an isolated web server for my services.

#### Nginx in Docker, the pros and cons
- Pros
1. Nginx can have some complex configurations, it will also conflict with the uhttpd if luci-app-nginx is installed.  
Docker just isolate it from the OpenWrt system.
- Cons
1. Nginx in Docker will have a little performance loss, while it is acceptable.



