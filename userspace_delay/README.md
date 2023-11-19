### Userspace Application

This is an example implementation of a User Space application that communicates with the QDISC through a Character Device.

### Usage
```
	sudo python3 userspace_delay.py <path_to_chardev>
```

```
usage: userspace_delay.py [-h] [-i INTERVAL] [-m MINCOUNT] device

positional arguments:
  device                Character Device that corrosponds to the QDISC instance.

options:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        Interval in seconds in which to check free space inside the QDISC
  -m MINCOUNT, --mincount MINCOUNT
                        Minimum count of free elements in QDISC
```