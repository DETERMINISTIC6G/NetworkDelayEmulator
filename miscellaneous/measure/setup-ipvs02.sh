sudo ip netns add switch

sudo ip link set ens1f2 netns switch
sudo ip link set ens1f3 netns switch

sudo ip netns exec switch /bin/bash -c 'ip a add 10.0.0.2/24 dev ens1f2'
sudo ip netns exec switch /bin/bash -c 'ip link set dev ens1f2 up'

sudo ip netns exec switch /bin/bash -c 'ip a add 20.0.0.1/24 dev ens1f3'
sudo ip netns exec switch /bin/bash -c 'ip link set dev ens1f3 up'

sudo ip netns exec switch /bin/bash -c 'sysctl -w net.ipv4.ip_forward=1'
