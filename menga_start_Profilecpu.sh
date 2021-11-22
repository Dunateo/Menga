#!/bin/bash

# Setting up global variable
NB_ARGS=-1
FIRST_OPT=-1
FIRST_VAL=-1
SECOND_OPT=-1
SECOND_VAL=-1
THIRD_OPT=-1
THIRD_VAL=-1
FOURTH_OPT=-1
FOURTH_VAL=-1

# Setting up the container global variable
CONTAINER_PID=-1
CONTAINER_ID=-1
CONTAINER_NAME="-1"

# Setting up the profile.py arguments
FREQ=99
SEC=15
OUT="./perf.svg"


function help {
    # Print help for menga
    clear
    echo ""
    test_figlet=`figlet HELP`
    if [ "$?" -eq 0 ]
    then
        figlet HELP
    else
        echo "--------"
        echo "| HELP |"
        echo "--------"
        echo ""
    fi
    echo "----------------"
    echo "| First option |"
    echo "----------------"
    echo ""
    echo "-id id_value_of_docker_container"
    echo "-pid pid_value_of_docker_container"
    echo "-name name_of_docker_container (name must be unique)"
    echo ""
    echo "--------------------------------"
    echo "| Second, third, fourth option |"
    echo "--------------------------------"
    echo ""
    echo "-freq (default value is 99)"
    echo "-sec (default value is 15)"
    echo "-out path_to_the_output_file (default value is \"./perf.svg\")"
    echo ""
}

function analyse_cpu {
    # Verify the container PID
    if [ $CONTAINER_PID -ne "-1" ]
    then
        # Launch CPU analysis
        ./bcc/tools/profile.py -dF $FREQ -f $SEC -p $CONTAINER_PID | ./FlameGraph/flamegraph.pl > $OUT
    else
        echo "Container PID is wrong"
    fi
}

function verif_existing_args {
    nb=-1

    # Verify the -id option
    if [ $FIRST_OPT = "-id" ]
    then
        nb=`docker ps | grep -v grep | grep "$FIRST_VAL" | wc -l`

        # If the command result doesn't contain 1 line
        if [ $nb -ne 1 ]
        then
            echo "ID not valid"
            exit 1
        else
            test_name_docker=`docker ps | grep -v grep | grep "$FIRST_VAL" | awk '{print $2}'`
            nb=`ps -edf | grep -v grep | grep "$test_name_docker" | wc -l`

            # If the command result doesn't contain 1 line
            if [ $nb -ne 1 ]
            then
                echo "Name not valid"
                exit 1
            else
                ID_option
                verif_profile_args
            fi
        fi
    # Verify the -pid option
    elif [ $FIRST_OPT = "-pid" ]
    then
        nb=`ps -edf | grep -v grep | grep "$FIRST_VAL" | wc -l`

        # If the command result doesn't contain 1 line
        if [ $nb -ne 1 ]
        then
            echo "PID not valid"
            exit 1
        else
            PID_option
            verif_profile_args
        fi
    # Verify the -name option
    elif [ $FIRST_OPT = "-name" ]
    then
        nb=`ps -edf | grep -v grep | grep "$CONTAINER_NAME" | wc -l`

        # If the command result doesn't contain 1 line
        if [ $nb -ne 1 ]
        then
            echo "Name not valid"
            exit 1
        else
            NAME_option
            verif_profile_args
        fi
    # If not the available option
    else
        echo "Option not available"
    fi
}

function ID_option {
    CONTAINER_NAME=`docker ps | grep -v grep | grep "$FIRST_VAL" | awk '{print $2}'`
    CONTAINER_PID=`ps -edf | grep -v grep | grep "$CONTAINER_NAME" | awk '{print $2}'`
}

function PID_option {
    CONTAINER_PID=$FIRST_VAL
}

function NAME_option {
    CONTAINER_PID=`ps -edf | grep -v grep | grep "$CONTAINER_NAME" | awk '{print $2}'`
}

function verif_profile_args {
    # Verify the -freq option
    if [ $SECOND_OPT = "-freq" ]
    then
        echo $SECOND_VAL
        
        # Verify the -sec option
        if [ $THIRD_OPT = "-sec" ]
        then
            echo $THIRD_VAL
            
            # Verify the -out option
            if [ $FOURTH_OPT = "-out" ]
            then
                echo "$FOURTH_VAL"
            # Verify the -1 option
            elif [ $FOURTH_OPT = "-1" ]
            then
                echo "No other arguments"
            # If not an available option
            else
                echo "Option not available"
            fi

        # Verify the -out option
        elif [ $THIRD_OPT = "-out" ]
        then
            echo $THIRD_VAL

            # Verify the -out option
            if [ $FOURTH_OPT = "-sec" ]
            then
                echo $FOURTH_VAL
            # Verify the -1 option
            elif [ $FOURTH_OPT = "-1" ]
            then
                echo "No other arguments"
            # If not an available option
            else
                echo "Option not available"
            fi

        # Verify the -1 option
        elif [ $THIRD_OPT = "-1" ]
        then
            echo "No other arguments"
        # If not an available option
        else
            echo "Option not available"
        fi

    # Verify the -sec option
    elif [ $SECOND_OPT = "-sec" ]
    then
        echo $SECOND_VAL

        if [ $THIRD_OPT = "-freq" ]
        then
            echo $THIRD_VAL

            # Verify the -out option
            if [ $FOURTH_OPT = "-out" ]
            then
                echo "$FOURTH_VAL"
            # Verify the -1 option
            elif [ $FOURTH_OPT = "-1" ]
            then
                echo "No other arguments"
            # If not an available option
            else
                echo "Option not available"
            fi

        # Verify the -out option
        elif [ $THIRD_OPT = "-out" ]
        then
            echo "$THIRD_VAL"

            # Verify the -freq option
            if [ $FOURTH_OPT = "-freq" ]
            then
                echo $FOURTH_VAL
            # Verify the -1 option
            elif [ $FOURTH_OPT = "-1" ]
            then
                echo "No other arguments"
            # If not an available option
            else
                echo "Option not available"
            fi

        # Verify the -1 option
        elif [ $THIRD_OPT = "-1" ]
        then
            echo "No other arguments"
        # If not an available option
        else
            echo "Option not available"
        fi

    # Verify the -out option
    elif [ $SECOND_OPT = "-out" ]
    then
        echo "$SECOND_VAL"

        if [ $THIRD_OPT = "-freq" ]
        then
            echo $THIRD_VAL

            # Verify the -sec option
            if [ $FOURTH_OPT = "-sec" ]
            then
                echo $FOURTH_VAL
            # Verify the -1 option
            elif [ $FOURTH_OPT = "-1" ]
            then
                echo "No other arguments"
            # If not an available option
            else
                echo "Option not available"
            fi

        # Verify the -sec option
        elif [ $THIRD_OPT = "-sec" ]
        then
            echo $THIRD_VAL

            # Verify the -freq option
            if [ $FOURTH_OPT = "-freq" ]
            then
                echo $FOURTH_VAL
            # Verify the -1 option
            elif [ $FOURTH_OPT = "-1" ]
            then
                echo "No other arguments"
            # If not an available option
            else
                echo "Option not available"
            fi

        # Verify the -1 option
        elif [ $THIRD_OPT = "-1" ]
        then
            echo "No other arguments"
        # If not an available option
        else
            echo "Option not available"
        fi

    # Verify the -1 option
    elif [ $SECOND_OPT = "-1" ]
    then
        echo "No other arguments"
    # If not an available option
    else
        echo "Option not available"
    fi
}

# Verify the number of arguments
if [ "$#" -lt "2" ]
then
    if [ "$#" -eq "1" ] && [ $1 = "-help" ]
    then
        help
    else
        echo "Not enough arguments"
    fi
else
    NB_ARGS=$#
    # Verify that the number of arguments are pair
    if [ `expr $NB_ARGS % 2` -eq 0 ]
    then
        # Launch retrievation of arguments
        if [ $NB_ARGS -ge 2 ]
        then
            FIRST_OPT=$1
            FIRST_VAL=$2
        fi

        if [ $NB_ARGS -ge 4 ]
        then
            SECOND_OPT=$3
            SECOND_VAL=$4
        fi
        
        if [ $NB_ARGS -ge 6 ]
        then
            THIRD_OPT=$5
            THIRD_VAL=$6
        fi

        if [ $NB_ARGS -eq 8 ]
        then
            FOURTH_OPT=$7
            FOURTH_VAL=$8
        fi
        # Launch verication of arguments
        verif_existing_args
    else
        echo "Arguments impair"
        exit 1
    fi
fi
