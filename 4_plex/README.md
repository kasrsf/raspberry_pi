# Setup Plex Media Server

# Steps

1. **Updating the system**
```bash
sudo apt update
sudo apt upgrade
```

2. **Install HTTPS Transport Package:**
* Plex repository uses HTTPS, so ensure that the HTTPS transport package is installed:
```bash
sudo apt-get install apt-transport-https
```

3. **Add the Plex Media Server Repository:**
* First, add the Plex GPG key to your system:
```bash
curl https://downloads.plex.tv/plex-keys/PlexSign.key | sudo apt-key add -
```
* Then, add the Plex repository to your sources list:
```bash
echo deb https://downloads.plex.tv/repo/deb public main | sudo tee /etc/apt/sources.list.d/plexmediaserver.list
```

4. **Install Plex Media Server:**
* Update your package lists again:
```bash
sudo apt update
```
* Install Plex Media Server:
```bash
sudo apt install plexmediaserver
```
* The installation process for Plex sets up a few different things for us:
    * it creates a user and group for Plex to run under. This user and group is called `plex`
    * it also will setup two directories, one where to store files temporarily that Plex is transcoding. You can find this folder at `/var/lib/plexmediaserver/tmp_transcoding`
    The second directory is where Plex will store all the metadata it retrieves for your media. This folder can be found at `/var/lib/plexmediaserver/Library/Application Support` [^1]

5. **Configure Permissions for External Drive:**
* we need to ensure the newly created `plex` user has read (and possibly write access to the media directories)
    * the existing groups where the `plex` user falls under can be checked with `groups plex`
    ```bash
    groups plex
    > plex : plex video
    ```

    * we can then check the owner group and user of the mounted external drive with `ls -l /mount/point/path`
    the mount point can be retrieve with `df -h`

    * we can either create a new user group with ownership permissions to the mounted drive or add the `plex` user to the existing owner group

    * the `plex` user can be added to the existing owner group with
    ```bash
    sudo usermod -a -G owner_group plex
    ```

6. **Enable and Start Plex Media Server:**
* Plex should start automatically after installation, but we can ensure it's enabled and running with:
```bash
sudo systemctl enable plexmediaserver
sudo systemctl start plexmediaserver
```

7. **Access Plex Web Interface:**
Open a browser and navigate to `http://your_raspberry_pi_IP_address:32400/web` and complete the Plex setup wizard



[^1]: https://pimylifeup.com/raspberry-pi-plex-server/
