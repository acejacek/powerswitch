# PowerSwitch
Python program to control relay connected to GPIO.

Check usage:
```
python powerswitch.py --help
```

## usage with Shairport-Sync

If `powerswitch.py` needs to cooperate with audioboards stacked on top of GPIOs, consult the documentation. Some of the GPIOs are reserved by board:

- [GPIO Usage of HiFiBerry Boards](https://www.hifiberry.com/build/documentation/gpio-usage-of-hifiberry-boards/)


Edit configuration file `/etc/shairport-sync.conf`. Modify `sessioncontrol` section:

```
// Advanced parameters for controlling how a Shairport Sync runs
sessioncontrol = 
{
run_this_before_play_begins = "/usr/bin/python /home/pi/powerswitch/powerswitch.py --relay-pin 16 --power-on";
run_this_after_play_ends = "/usr/bin/python /home/pi/powerswitch/powerswitch.py --relay-pin 16 --power-off --delay 600";
};
```
Set correct pin number.

Remember to grant access to GPIO for user `shairport-sync`. Add him to `gpio` group. 
```
sudo usermod -a -G gpio shairport-sync
```

Finally, restart `shairport-sync` service:
```
sudo service shairport-sync restart
```
