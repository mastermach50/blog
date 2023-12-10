# Dual Booting NixOS and Windows 11 (with SecureBoot)

> Please do not "follow" this guide. Read the entirety of it and then make your own informed decisions.

> I am not sponsored by anyone, I am writing this on my own accord and the links here were chosen without any bias. I am not liable for any damages.

> for any corrections create an issue on the github repo of this page

## My Current Setup (AKA your end result)
I am currently running Windows 11 and NixOS 23.11 on the same laptop on the same NVME drive. I am using `systemd-boot` as my bootloader to easily switch between my Windows and NixOS installations. [Secure Boot](https://en.wikipedia.org/wiki/UEFI#Secure_Boot) was enabled using [lanzaboote](https://github.com/nix-community/lanzaboote).

## Preface (Do Not Skip This)
You will need to wipe your disk so first of all **backup you data**.

> ALWAYS BACKUP YOUR DATA

For dual booting, the Windows install instructions is a bit different so do read through it.

First you will be installing Windows and then NixOS. Since NixOS does not support secureboot out of the box yet you will have to make it work by installing [lanzaboote](https://github.com/nix-community/lanzaboote).

### Some General Tips

- The NixOS documentation may or may not be up to date so do not blindly depend on it.
- Having full disk encryption (bitlocker on Windows) is good, but when dual booting things may go wrong, sometimes after a long time so not having bitlocker enabled will make recovering your files a lot easier. Still, use bitlocker if you have to.

## Windows Installation

### Preparing the ISO
A regular Windows ISO will do.

To flash the ISO to a USB drive I used [Rufus](https://rufus.ie) form another Windows machine. If you are using rufus then before flashing the iso to a usb drive rufus will give you the option to disable bitlocker encryption, you should disable bitlocker encryption. If you did not get this option then continue as bitlocker can be disabled after installing Windows.

If you are not using rufus then after installing Windows you will have to go into the settings and disable bitlocker encryption form there. (Refer **After Installing Windows** section)

> You can enable bitlocker from Windows after installing both Windows and NixOS and installing lanzaboote.

> **Disabling bitlocker is important** for the install process beacuse bitlocker depends on secureboot and we need to disable secureboot for installing NixOS. If secure boot is disabled and you have enabled bitlocker you won't be able to boot into Windows.

### Installing Windows

During Windows installation select `Custom: Install Windows Only (advanced)`. You will be asked select which drive to install to and to setup the partitions. You will need to setup a large EFI partition (500MB to 1GB) for dualbooting as the default EFI partition size on Windows is just 100MB. You can do this by following this guide.

https://www.ctrl.blog/entry/how-to-esp-Windows-setup.html

> If you are ever planning to dual boot anything with Windows please consider creating a large EFI partition during Windows install.

> I have gone with a 1GB EFI partition on my system

### After Installing Windows

If you have not disabled bitlocker from rufus or used another tool to flash the iso or did not get the disable bitlocker option in rufus the it is time to do it now. Follow this guide if you are not sure how to do it.

https://Windowsreport.com/disable-bitlocker-Windows-11/

Now you will have to shrink the current Windows partition to make space for NixOS. If you are not sure how to do it the follow this guide.

> The guide shows you different methods to shrink / expand partitions, but you only need to shrink the partition.

> You will need to shrink the partition for as much space you need because resizing partitions after installing both OSs might not be feasable.

https://www.howtogeek.com/212/resize-a-partition-on-Windows/

## NixOS Installation

### Before Installation

- Make sure that **bitlocker is disabled** on Windows.
- Make sure that you have shrank the Windows partition to make space for NixOS
> ⚠️ **DO NOT PROCEED without this**

Now you will need to **disable secure boot** from the system's BIOS. The process for this wiil be different based on your system's manufacturer so please look it up and do the necessary.

You will have to flash the NixOS ISO to a usb drive and boot into it. Again booting from a usb drive will be different based on your system's manufacturer so please look it up and do the necessary.

### Installing NixOS

During installation you will be asked to which partition NixOS should be installed. Here select replace a partition. On the partition figure given below that click on the unallocated space that you just made by shrinking the Windows partition. Continue the installation and you will have NixOS installed with systemd-boot as the bootloader.

> Be careful when doing this step, do not select the wrong partition.

### After Installing NixOS

You have to now go to the bios again and set the default boot option as *Linux Boot Manager*. Now when you boot the system you will be able to select which OS you want to boot into.

But now we have a problem,
- Secure boot is not enabled. If it is enabled again then we cannot boot into NixOS anymore.

To overcome this we have to setup NixOS for secure boot, For this we are going to use a project called [lanzaboote](https://github.com/nix-community/lanzaboote).

## Installing Lanzaboote

Do not follow the instructions for installing lanzaboote from the NixOS wiki as this might be out of date and definitely **DO NOT select reset all secureboot keys** anywhere in the bios (you will get what I mean from the lanzaboote docs).

You will have to follow the lanzaboote docs to install lanzaboote onto your NixOS system. For this simply follow the lanzaboote docs.

https://github.com/nix-community/lanzaboote/blob/master/docs/QUICK_START.md

> There are two methods given in the lanzaboote docs to install secureboot, one using nix flakes and another using niv. The niv method was the one that worked for me.

If you followed all the instructions properly you should have a system that can dual boot NixOS and Windows and has secure boot enabled.

## After All is Said and Done

Refer only the **System Time** section from this NixOS wiki page, the rest was already done properly during this guide.

https://NixOS.wiki/wiki/Dual_Booting_NixOS_and_Windows

Here are some general tips for using your dual bootable system

- To clear NixOS generations from the systemd-boot screen you need to run the `nix-collect-garbage` command both as a root and regular user and then rebuild the system.
- In systemd-boot during the OS selection screen use the arrow keys to navigate to the entry you want to make the deafult (like Windows 11) and press `d` to make it the default. You can also increase and decrease the time needed to autoselect the default entry by pressing `t` and `shift +t` respectively.
- If you want to switch from Windows to NixOS it is better to select reboot from the start menu rather that shutdown and then power on again because during shutdown Windows stores some data on the disk and then reads it again during startup, this can cause the system to bluescreen (very rarely) if after the shutdown you boot into another OS (NixOS in this case) and then boot back into Windows. If you select reboot from the start menu then the system does a clean restart instead of these shenanigans.