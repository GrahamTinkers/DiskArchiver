# Disk Archiver Project

The Disk Archiver project is based on an old 3.5” floppy disk autoloader, the Disketten Autoloader C4, produced by LSK Data System GmbH. When I first received the unit, I didn’t have a clear plan for its use. However, a few weeks later, I remembered watching a video by Shelby on his Tech Tangents YouTube channel about the Greaseweazle and KryoFlux. That inspired me to transform the autoloader into a device for backing up disks rather than duplicating them.

To start, I purchased a Greaseweazle, connected it to a Raspberry Pi 3, and began experimenting with Python code. I used the code to control the autoloader’s mechanism via serial commands and had the Greaseweazle read the disks and save the files. Later, I added a Pi Camera to take photos of the disk labels, which helps with identifying the disks more easily during backup retrieval.

The autoloader, along with a standalone disk duplicator, was originally offered by a member of the Berlin Creators makerspace. They were looking to give them away before taking them to a recycling center (BSR). I’m glad I saved them!

Today, the Disk Archiver resides at the [Berlin Creators makerspace](https://berlincreators.de/) the site is only in German, but you can translate it. Anyone is welcome to stop by during open hours (check their website) and back up their old 3.5” disks. Just bring along a USB flash drive to store the disk images. 

Read the [Tom’s Hardware Article](https://www.tomshardware.com/raspberry-pi/this-raspberry-pi-automatically-archives-a-stack-of-amiga-floppy-disks)

Watch the [YouTube](https://youtu.be/UrLrj-g-TfE) video.

The Disk Archiver was nicknamed the Copy Bot Pro and was unvailed at VCFB 2024, the below image was taken at the [Vintage Computing Festival Berlin (VCFB) 2024](https://vcfb.de/2024/)

![DCP2](https://github.com/user-attachments/assets/e7fc9fa6-c1c4-49e0-8778-c863b5fd6bae)
