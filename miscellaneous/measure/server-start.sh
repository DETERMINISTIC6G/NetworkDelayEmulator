CMD1=""
CMD2=""
CMD3=""
CMD4=""
CMD5=""
CMD6=""

CMD1="sudo dmesg --follow"
CMD2="htop"
CMD3="slurm -i ens1f3"
CMD4="./scripts/send.sh 1 1000000 0.000005"
CMD5="python3 scripts/receive-delay.py"
CMD6="watch -n 0.25 tc -p -d -s qdisc show dev ens1f3"

tmux kill-session -t ba

tmux new-session -d -s ba
tmux split-window -h -p 70 -t ba.0
tmux split-window -h -t ba.1

tmux split-window -v -p 70 -t ba.2
tmux split-window -v -t ba.3

tmux split-window -v -t ba.1
#tmux split-window -v -t ba.2

tmux  send-keys -t ba.0 "ssh ipvs02" C-m
#tmux  send-keys -t ba.1 "ssh ipvs01" C-m
tmux  send-keys -t ba.2 "ssh ipvs01" C-m

tmux  send-keys -t ba.3 "ssh ipvs01" C-m
tmux  send-keys -t ba.4 "ssh ipvs01" C-m
tmux  send-keys -t ba.5 "ssh ipvs02" C-m

tmux  send-keys -t ba.0 "bash" C-m
#tmux  send-keys -t ba.1 "sudo ip netns exec sender /bin/bash" C-m
tmux  send-keys -t ba.2 "sudo ip netns exec receiver /bin/bash" C-m

tmux  send-keys -t ba.3 "sudo ip netns exec sender /bin/bash" C-m
tmux  send-keys -t ba.4 "sudo ip netns exec receiver /bin/bash" C-m
tmux  send-keys -t ba.5 "sudo ip netns exec switch /bin/bash" C-m

sleep 1

tmux  send-keys -t ba.0 "$CMD1" C-m
tmux  send-keys -t ba.1 "$CMD2" C-m
tmux  send-keys -t ba.2 "$CMD3" C-m

tmux  send-keys -t ba.3 "$CMD4"
tmux  send-keys -t ba.4 "$CMD5" C-m
tmux  send-keys -t ba.5 "$CMD6" C-m

tmux set -g mouse on

tmux a -t ba
