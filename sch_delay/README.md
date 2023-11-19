Prerequisites

In order to compile the Kernel Module, you need the latest Kernel Headers for your specific Kernel. You can install them on Debian-based systems using the following command:
```
    sudo apt install linux-headers-$(uname -r)
```
### Installation

1. Clone this repository:
```
    git clone <REPO LINK>
```
2. Switch into the delay_sch directory
```
    cd sch_delay
```
3. Compile the Kernel Module
```
    make clean && make
```
4. You can now load and unload the Kernel Module using the following command:

Load:
```
    sudo insmod build/sch_delay.ko
```
Unload:
```
    sudo rmmod sch_delay
```

### Usage

You can add the QDISC to a device using a command like this:
```
    sudo tc qdisc add dev <interface> root delay reorder <True/False> limit <int>
```

To remove the QDISC from the device:
```
    tc qdisc del dev <interface> root
```
You need to remove the QDISC from all devices befor you can unload the Kernel Module


Note that in order to supply arguments to the QDISC you need to use a custom version of ```tc``` as explained [here](../tc/README:md)


Once assigned, a Character Device is created in ```/dev/sch_delay/<interface_name>```. 

### Configuration

The QDISC can be configured via the ```tc``` command using a command like this:
```
    sudo tc qdisc change dev <interface> root delay <option> <value>
```

Available Options:
| Option | Type | Default | Explanation                    |
|--------|------|---------| ------------------------------ |
| limit  | int  | 1000    | The size of the internal queue |
| reorder| bool | true    | Whether packages should be sent in a order received or ordered by smallest delay |

Note that this functionallity does also require a custom version of ```tc``` as explained [here](../tc/README:md)

### Troubleshooting
Errors during the QDISCs operation are logged into the Kernel Log, accessible via
```
    sudo dmesg
```
