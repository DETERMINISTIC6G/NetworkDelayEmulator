DATA_DIR="./data"

DISTRIBUTION_OPTIONS=(
#    "700us_normal_distributed_delay"
    "200us_25us_normal_distributed"
    "99_1ms_static"
    "100us_static"
    "050us_static"
    "000_no_delay"
    "custom"
)
DISTRIBUTION_OPTIONS_NAME=(
    "\"Normal Distributed µ: 200us, σ: 25us\""
    "\"Static Delay of 1ms\""
    "\"Static Delay of 100us\""
    "\"Static Delay of 50us\""
    "\"No Delay\""
    "\"Custom\""
)

DATA_OPTIONS_NAME=(
    "System_Default_(pfifo_fast)"
    "Reference_Data"
    "Sch_Delay_FIFO"
    "Sch_Delay_Reordered"
    "Netem"
)
DATA_OPTIONS=(
    "system_default"
    "reference_data"
    "sch_delay_fifo"
    "sch_delay_reordered"
    "netem"
)

BANDWITH_OPTIONS=(
#    "31Mbps"
#    "91Mbps"
    "101Mbps"
#    "260Mbps"
)


plot_menu () {
    PLOT=""
    cmd=(dialog --keep-tite --menu "Select Option:" 22 76 16)
    options=(
            1 "Distribution Hist"
            2 "Boxplot"
            3 "Distribution Lines"     
            4 "Russland"     
        )

    choices=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
    clear
    case $choices in
        1)
            PLOT="distribution_hist.py"
            ;;
        2)
            PLOT="boxplot.py"
            ;;
        3)
            PLOT="distribution_lines.py"
            ;;
        4)
            PLOT="russland.py"
            ;;
        "")
            echo "Bye"
            exit 0
            ;;
        *)
         echo "ERRROR"
         exit 1
         ;;
    esac
}

bandwith_menu () {
    BANDWITH=""
    cmd=(dialog --keep-tite --menu "Select inventory:" 22 76 16)
    options=()
    count=1
    for inv in "${BANDWITH_OPTIONS[@]}"; do
        options=(${options[@]} $count $inv)
        ((count++))
    done

    choices=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)

    clear
    
    if [ -z "$choices" ] 
    then
        exit 1
    fi

    case $choices in
        *)
            BANDWITH="${BANDWITH_OPTIONS[((choices-1))]}"
            ;;
        esac
}

distribution_menu () {
    DISTRIBUTION=""
    DISTRIBUTION_NAME=""
    cmd=(dialog --keep-tite --menu "Select Option:" 22 76 16)
    options=()
    count=1
    for ((x = 0; x < ${#DISTRIBUTION_OPTIONS_NAME[@]}; x++)); do
        options=("${options[@]}" $count "${DISTRIBUTION_OPTIONS_NAME[$x]}")
        echo $count ${DISTRIBUTION_OPTIONS_NAME[$x]}
        echo ${options[@]}
        ((count++))
    done
    choices=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)



    clear
    
    if [ -z "$choices" ] 
    then
        exit 1
    fi

    case $choices in
        *)
            DISTRIBUTION="${DISTRIBUTION_OPTIONS[((choices-1))]}"
            DISTRIBUTION_NAME="${DISTRIBUTION_OPTIONS_NAME[((choices-1))]}"

            ;;
        esac
}


data_menu () {
    DATA=""
    cmd=(dialog --separate-output --checklist  "Select Data Source:" 22 76 16)
    options=(1 "ALL" off)
    count=2
    for ((x = 0; x < ${#DATA_OPTIONS_NAME[@]}; x++)); do
        options=(${options[@]} $count ${DATA_OPTIONS_NAME[$x]} off)
        ((count++))
    done


    choices=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)

    clear
    
    if [ -z "$choices" ] 
    then
        echo "You need to select at least one Inventory"
        exit 1
    fi

    for choice in $choices
    do
        case $choice in
            1)
                
                for (( x=0; x<="${#DATA_OPTIONS_NAME[@]}"-1; x++)); do
                    DATA="$DATA --name \"${DATA_OPTIONS_NAME[$x]}\" --file data/${DISTRIBUTION}_${BANDWITH}_${DATA_OPTIONS[$x]}.csv"
                done           
                break;
                ;;
            *)
                DATA="$DATA --name \"${DATA_OPTIONS_NAME[((choice-2))]}\" --file data/${DISTRIBUTION}_${BANDWITH}_${DATA_OPTIONS[((choice-2))]}.csv"
                ;;
            esac
    done
}

custom_menu () {
    DATA=""
    FILES=()
    options=()
    cmd=(dialog --separate-output --checklist  "Select Data Sources:" 22 76 16)
    count=0
    for file in `ls $DATA_DIR/*.csv | xargs -n 1 basename`; do
        echo $file
        options=(${options[@]} $count $file off)
        FILES=(${FILES[@]} $file)
        ((count++))
    done

    choices=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)

    clear
    
    if [ -z "$choices" ] 
    then
        echo "You need to select at least one Inventory"
        exit 1
    fi

    for choice in $choices; do
        filename=${FILES[$choice]}
        name=$(dialog --title "Name for $filename" --inputbox "$filename Name:" 8 40 3>&1 1>&2 2>&3 3>&-)
        DATA="$DATA --name "$name" --file $DATA_DIR/$filename"
    done  
    BANDWITH="Mixed"
    echo $DATA
}

size_menu () {
SIZE=$(\
  dialog --title "Number of Packages" \
         --inputbox "Number of Packages:" 8 40 5000000\
  3>&1 1>&2 2>&3 3>&- \
)
clear
}


plot_menu
distribution_menu

if [[ "$DISTRIBUTION" == "custom" ]]; then
    BANDWITH_OPTIONS=(${BANDWITH_OPTIONS[@]} "Mixed")
fi

bandwith_menu

if [[ "$DISTRIBUTION" == "custom" ]]; then
    custom_menu 
else
    data_menu
fi

size_menu

echo Distribution: $DISTRIBUTION_NAME: $DISTRIBUTION
echo Bandwith: $BANDWITH
echo Plot Script: $PLOT
echo Size: $SIZE
echo Name: $NAME

cmd="python3 $PLOT --distribution $DISTRIBUTION --distribution_name $DISTRIBUTION_NAME --bandwith $BANDWITH $DATA --size $SIZE"
echo Executing script: $cmd
$cmd