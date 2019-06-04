# Dab and T-Pose Controlled Lights

Control your lights by dabbing and t-pose'ing, duh

## Getting the ZWave Controller working on the TX2

By default, I couldn't write to the `/dev/ttyACM0` device that the ZWave USB controller came up on with my NVDIA Tegra TX2.

You'll need to do something along the following to get permissions:

```bash
$ sudoedit /etc/udev/rules.d/50-myusb.rules
```

Followed by inserting the following lines to add perms to the `/dev/ttyUSB*` and `/dev/ttyACM*`:

```
KERNEL=="ttyUSB[0-9]*",MODE="0666"
KERNEL=="ttyACM[0-9]*",MODE="0666"
```
