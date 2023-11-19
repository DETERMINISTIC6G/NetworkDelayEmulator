sudo ip -all netns delete

sudo ip netns add sender
sudo ip netns add receiver

sudo ip link set ens1f2 netns sender
sudo ip link set ens1f3 netns receiver


sudo ip netns exec sender /bin/bash -c 'ip a add 10.0.0.1/24 dev ens1f2'
sudo ip netns exec sender /bin/bash -c 'ip link set dev ens1f2 up'
sudo ip netns exec sender /bin/bash -c 'ip route add 20.0.0.0/24 via 10.0.0.2'


sudo ip netns exec receiver /bin/bash -c 'ip a add 20.0.0.2/24 dev ens1f3'
sudo ip netns exec receiver /bin/bash -c 'ip link set dev ens1f3 up'
sudo ip netns exec receiver /bin/bash -c 'ip route add 10.0.0.0/24 via 20.0.0.1'


#sudo ip a add 10.0.0.1/24 dev enp2s0f0
#sudo ip netns exec sender /bin/bash -c 'ip a add 10.0.0.2/24 dev enp2s0f1'
#sudo ip link set dev enp2s0f0 up
#sudo ip netns exec test /bin/bash -c 'ip link set dev enp2s0f1 up'
