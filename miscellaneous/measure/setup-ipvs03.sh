export LD_LIBRARY_PATH=/opt/napatech3/lib

tmux has-session -t ntservice 2>/dev/null

if [ $? != 0 ]; then
    tmux new-session -s ntservice -d
    tmux send-keys -t ntservice.0 "sudo LD_LIBRARY_PATH=/opt/napatech3/lib /opt/napatech3/bin/ntservice" C-m

fi
