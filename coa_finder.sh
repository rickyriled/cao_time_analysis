#!/bin/bash

N=$1

# Clear the (per trialn) jsons ahead of time
echo "clearing folder/computing indexing.."
rm -rf indiv_timekey_folder/H1_keys/*
rm -rf indiv_timekey_folder/L1_keys/*
rm -rf indiv_timekey_folder/V1_keys/*

rm -rf joined_timekey_folder/*

rm -rf plots/*


RA_N=$N
DEC_N=$((N/2))

echo "N=$N : ra_n=$RA_N : dec_n=$DEC_N"
echo " "
echo " "

echo "looping new_2.."
echo " "
for (( i=0; i<$RA_N ; i++));
do
    for (( j=0; j<$DEC_N ; j++));
    do
        echo "case: $i , $j"
        python3 max_time.py --det "L1" --ra $i --dec $j --N $N &
        python3 max_time.py --det "V1" --ra $i --dec $j --N $N &
        python3 max_time.py --det "H1" --ra $i --dec $j --N $N &
        echo " "
        echo " "
    done 
    
done



echo "L1 monitor.."
python3 monitor.py --directory "indiv_timekey_folder/L1_keys/" --dir_length $(((RA_N)*(DEC_N)))

echo "V1 monitor.."
python3 monitor.py --directory "indiv_timekey_folder/V1_keys/" --dir_length $(((RA_N)*(DEC_N)))

echo "H1 monitor.."
python3 monitor.py --directory "indiv_timekey_folder/H1_keys/" --dir_length $(((RA_N)*(DEC_N)))

echo " "


echo "joining L1.."
python3 json_stack_keys.py --jsons_path "indiv_timekey_folder/L1_keys/" --merge_path_name "joined_timekey_folder/L1"

echo "joining V1.."
python3 json_stack_keys.py --jsons_path "indiv_timekey_folder/V1_keys/" --merge_path_name "joined_timekey_folder/V1"

echo "joining H1.."
python3 json_stack_keys.py --jsons_path "indiv_timekey_folder/H1_keys/" --merge_path_name "joined_timekey_folder/H1"

echo " "
echo "making plots..."

python3 plot_maker.py


echo "done!"
