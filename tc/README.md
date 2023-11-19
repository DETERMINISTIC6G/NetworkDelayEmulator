### TC Module
If you want to change the behaviour of the QDISC you need to compile you own version of ```tc``` by following these stepps:

Note: This was tested for version ```v6.5.0``` of iproute2, but should also work with other versions.

1. Download the latest source of [iproute2](https://github.com/iproute2/iproute2/tags).

2. place the file ```code/tc/q_delay.c``` into the ```<iproute2_source>/tc/``` directory.

3. Either manually add the line ```TCMODULES += q_delay.o``` into the file ```<iproute2_source>/tc/Makefile``` or run the command ```patch -R <iproute2_source>/tc/Makefile <repo_path>/tc/Makefile.patch```.

4. Run Make in the  ```<iproute2_source>``` directory.

You can now use the ```tc``` binary in ```<iproute2_source>/tc/``` to interact with the QDISC.

## A word of caution
I would advise against replacing the installed version of iproute2 with this one, as any mistake could fully remove the machine's ability to communicate via the network, in most cases resulting in reinstalling the system.