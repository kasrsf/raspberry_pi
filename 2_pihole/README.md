# Setting up Pi-Hole for Netwok Ad-Blocker

# Steps

1. Update Raspberry Pi Packages

```bash
sudo apt update
sudo apt full-upgrade
```

2. Install Pi-Hole

Run the following single-line command to run the Pi-hole setup script:

```bash
curl -sSL https://install.pi-hole.net | bash
```

The setup script is relatively self-explanatory, but follow these tips if you aren’t sure how to proceed:

* When warned about needing a static IP address, click Continue to proceed; we’ll deal with this later
* When prompted to select an interface, select wlan0 to use your Raspberry Pi’s Wi-Fi connection
* When prompted to choose an upstream DNS provider, choose OpenDNS
* Include StevenBlack’s Unified Hosts List
* Install the Admin Web Interface
* Install lighttpd and the required PHP modules to run the Admin Web Interface
* Enable query logging
* When prompted to choose a privacy level, choose Anonymous mode

When you see “Installation complete!”, the setup is complete. This screen shows the IP address of your Pi-hole, a link to the admin interface, and your administrator password.

* Save this password somewhere safe, like a password manager — you’ll need it to work with your Pi-hole in the future
* Save the IP address — you’ll need it to configure a static IP address shortly
Pi-hole only provides a single administrator account, so there’s no username.

The admin interface can be accessed via `http://<:ip address>/admin`

3. Set Static IP for the Raspberry Pi on the network and set the static ip as the network's DNS server

# References

[1] [Block ads at home with Pi-hole](https://www.raspberrypi.com/tutorials/running-pi-hole-on-a-raspberry-pi/)