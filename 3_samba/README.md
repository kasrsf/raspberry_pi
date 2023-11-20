# Setup Samba to Access External Drive on Raspberry Pi

A Samba file server enables file sharing 
across different operating systems over a network. It lets you access your desktop files from a laptop and share files with Windows and macOS users. [^1]

Samba can be used to access an external hard drive connected to a Raspberry Pi from a mac on a local network:

## Setup

1. **Install Samba on Raspberry Pi**

```bash
sudo apt update
sudo apt install samba samba-common-bin
```

2. **Configure Samba**

* Edit the Samba configuration file `sudo nano etc/samba/smb.conf`
* At the end of the file, add the configuration for the external drive. For example:
```conf
[ExternalDrive]
path = /path/to/your/external/drive
writeable=Yes
create mask=0777
directory mask=0777
public=no
```
* Replace `/path/to/your/external/drive` with the actual apth to your mounted external drive. You can use the `df -h` command to get a human-readable format of file system disk space usage, which includes mount points

3. **Set up a Samba User:**
* You need to create a Samba user. This can be the same as your Raspberry Pi user (the username needs to exist as a Unix user).
* Run `sudo smpasswd -a yourusername` (replace `yourusername` with your actual username)
* Enter and confirm a password

4. **Restart Samba:**
* Restart the Samba service to apply changes: `sudo systemctl restart smbd`

5. **Access from Mac:**

* On your Mac, open Finder
* In the menu bar, go to `Go` > `Connect to Server`
* Type `smb://raspberrypi.local` (replace `raspberrypi.local` with the acutal hostname or IP address of your Raspberry Pi)
* Click `Connect`
* Enter the username and password you set up for Samba
* You should now see the external drive and be able to access its contents.

Mkae sure your Raspberry Pi and Mac are on the same local network and ensure your external drive is formatted in a file system that both the Raspberry Pi and Mac can read and write to.

[^1]: https://ubuntu.com/tutorials/install-and-configure-samba#1-overview

