## About this Project
This project is the implementation of a Linux Queuing Discipline for network delay implementation. This QDISC focuses on the ability to flexible delay packets following stochastic delay distributions that can be altered and fine-tuned to specific use cases.
The calculation of delays is outsourced to an application in User Space that pre-calculates delays and transfers them to the QDISC via a Character Device.

![Design](design.png)


## Getting Started
This project is divided into four parts:
1.  The Kernel Module that contains the QDISC:

    Files are contained in the ```sch_delay/sch_delay``` folder
    
    Installation/Usage is documented [here](sch_delay/README.md)

2.  A reference implementation of the User Space application:

    Files are contained in the ```sch_delay/userspace_delay``` folder

    Installation/Usage is documented [here](userspace_delay/README.md)

3.  A extension to the ```tc``` command to configure the QDISC:

    Files are contained in the ```sch_delay/tc``` folder

    Installation/Usage is documented [here](tc/README.md)

4.  A collection of miscellaneous scripts used during development and testing

    Files are contained in the ```sch_delay/miscellaneous``` folder

    Documentation [here](miscellaneous/README.md)

## A word of caution
This work has been tested with Kernel version ```6.1.0-10-amd64```. I expect it to also work with previous and upcoming kernel versions, but I cannot guarantee it. Use this Module at your own risk and be prepared for possible system crashes.
If you do use this Module, I advise you to use the ```sync``` command frequently to avoid the loss of unwritten data.
