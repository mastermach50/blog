---
title: Dual Booting NixOS and Windows (with SecureBoot)
author: MasterMach50
date: 21st July 2024
keywords: [ Windows, NixOS, Dual Boot, Secure Boot ]
description: A guide on how to dual boot NixOS and Windows with secure boot
---

> Please do not "follow" this guide. Read the entirety of it and then make your own informed decisions.

> I am not sponsored by anyone, I am writing this on my own accord and the links here were chosen without any bias. I am not liable for any damages.

> For any corrections create an issue on the github repo of this page

## My Current Setup (AKA your end result)
I am currently running Windows 11 and NixOS 24.11 on the same laptop on the same NVME drive. I am using `systemd-boot` as my bootloader to easily switch between my Windows and NixOS installations. [Secure Boot](https://en.wikipedia.org/wiki/UEFI#Secure_Boot) was enabled using [lanzaboote](https://github.com/nix-community/lanzaboote).

## Preface (Do Not Skip This)
You will need to wipe your disk so first of all **backup you data**.

> ALWAYS BACKUP YOUR DATA

For dual booting, the Windows install instructions is a bit different so do read through it.

First you will be installing Windows and then NixOS. Since NixOS does not support secureboot out of the box yet you will have to make it work by installing [lanzaboote](https://github.com/nix-community/lanzaboote).

### Some General Tips

- [https://nixos.wiki](https://nixos.wiki) may or may not be up to date so do not blindly depend on it.
- [https://wiki.nixos.org](https://wiki.nixos.org) is almost always up to date.
- Having full disk encryption (bitlocker on Windows) is good, but if things go wrong it will be harder to recover your data. It's still possibe to recover your data but a bit harder. Still, use bitlocker if you have to.

## Windows Installation

### Preparing the ISO
A regular Windows ISO will do.

To flash the ISO to a USB drive I used [Rufus](https://rufus.ie) form another Windows machine. If you are using rufus then before flashing the iso to a usb drive rufus will give you the option to disable bitlocker encryption, i recommend enabling this. If you did not get this option then continue as bitlocker can be disabled after installing Windows. (Refer **After Installing Windows** section)

> You can enable bitlocker from Windows after installing both Windows and NixOS and installing lanzaboote.

> **Disabling bitlocker is important** for the install process beacuse bitlocker depends on secureboot and we need to disable secureboot for installing NixOS. If secure boot is disabled and you have enabled bitlocker you won't be able to simply boot into Windows, you will have to get your bitlocker decryption key.

### Installing Windows

During Windows installation select `Custom: Install Windows Only (advanced)`. You will be asked select which drive to install to and to setup the partitions. You will need to setup a large EFI partition (500MB to 1GB) for dualbooting as the default EFI partition size on Windows is just 100MB which is too small for sual booting. You can do this by following this guide.

[https://www.ctrl.blog/entry/how-to-esp-windows-setup.html](https://www.ctrl.blog/entry/how-to-esp-windows-setup.html)

> If you are ever planning to dual boot anything with Windows please consider creating a larger EFI partition than what Windows defaults to during Windows install.

> I have gone with a 1GB EFI partition on my system

### After Installing Windows

If you have not disabled bitlocker from rufus or used another tool to flash the iso or did not get the disable bitlocker option in rufus then it is time to do it now. Follow this guide if you are not sure how to do it.

[https://www.howtogeek.com/805225/disable-bitlocker/](https://www.howtogeek.com/805225/disable-bitlocker/)

Now you will have to shrink the current Windows partition to make space for NixOS. If you are not sure how to do it the follow this guide.

[https://www.howtogeek.com/212/resize-a-partition-on-windows/](https://www.howtogeek.com/212/resize-a-partition-on-windows/)

> The guide shows you different methods to shrink / expand partitions, but you only need to shrink the partition.

> You will need to shrink the partition for as much space you need because resizing partitions after installing both OSs might not be feasable.

## NixOS Installation

### Before Installation

- Make sure that **bitlocker is disabled** on Windows.
- Make sure that you have shrank the Windows partition to make space for NixOS

> ⚠️ **DO NOT PROCEED WITHOUT THIS**

Now you will need to **disable secure boot** from the system's BIOS. The process for this will be different based on your system's manufacturer so please look it up and do the necessary.

You will have to flash the NixOS ISO to a usb drive and boot into it. I used [Rufus](https://rufus.ie) for this also. Again booting from a usb drive will be different based on your system's manufacturer so please look it up and do the necessary.

### Installing NixOS

During installation you will be asked to which partition NixOS should be installed. Here select replace a partition. On the partition figure given below that click on the unallocated space (grey colour) that you made by shrinking the Windows partition. Continue the installation and you will have NixOS installed with systemd-boot as the bootloader.

> Be careful when doing this step, do not select the wrong partition.

### After Installing NixOS

You have to now go to the bios again and set the default boot option as *Linux Boot Manager*. Now when you boot the system you will be able to select which OS you want to boot into.

But now we have a problem,
- Secure boot is not enabled. If it is enabled again then we cannot boot into NixOS using the Linux Boot Manager option anymore.

To fix this we have to setup NixOS for secure boot. For this we are going to use a project called [lanzaboote](https://github.com/nix-community/lanzaboote).

## Installing Lanzaboote

Do not follow the instructions for installing lanzaboote from the NixOS wiki as this might be out of date and definitely **DO NOT select reset all secureboot keys** anywhere in the bios (you will get what I mean from the lanzaboote docs).

You will have to follow the lanzaboote docs to install lanzaboote onto your NixOS system. For this simply follow the lanzaboote docs.

[https://github.com/nix-community/lanzaboote/blob/master/docs/QUICK_START.md](https://github.com/nix-community/lanzaboote/blob/master/docs/QUICK_START.md)

> There are two methods given in the lanzaboote docs to install secureboot, one using nix flakes and another using niv. Use the niv method if you are not using nix flakes to configure your system.

If you followed all the instructions properly you should have a system that can dual boot NixOS and Windows and has secure boot enabled.

## After All is Said and Done

[https://wiki.nixos.org](https://wiki.nixos.org) provides some general tips for NixOS and Windows dual booters [here](https://wiki.nixos.org/wiki/Dual_Booting_NixOS_and_Windows). It also talks about things like how to make the bootloader detect Windows (In our case Windows would be automatically detected), how to use grub instead of systemd-boot as the bootloader and about dual booting using different drive configurations.

Refer to the **System Time** section from [https://wiki.nixos.org](https://wiki.nixos.org) to make sure that time on Windows remains in sync when dualbooting.

[https://wiki.nixos.org/wiki/Dual_Booting_NixOS_and_Windows#System_time](https://wiki.nixos.org/wiki/Dual_Booting_NixOS_and_Windows#System_time)

## General Tips

Here are some general tips for using your dual bootable system

- To clear NixOS generations from the systemd-boot screen you need to run the `nix-collect-garbage` command and then also rebuild the system.
- systemd-boot has some keyboard shortcuts to set an entry as the default entry, set the time to auto select the default entry etc. You can find that [here](https://systemd.io/BOOT/).
- If you want to switch from Windows to NixOS while in Windows instead of powering off and the starting the system select reboot from Windows. In Windows powering off and then on again is not the same as a reboot [Shutting Down Doesn't Fully Shut Down Windows 10](https://www.howtogeek.com/349114/shutting-down-doesnt-fully-shut-down-windows-10-but-restarting-it-does/). Although there is no actual proof that restarting is better to switch from Windows to another OS I still recommend restarting to switch to a different OS.