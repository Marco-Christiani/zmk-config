#!/usr/bin/bash

# Run from zmk/app in container
config_dir="/home/marco/Github/zmk-config/config"
printf "Building Left"
printf '=%.0s' {1..30}
printf "\n"
west build -d build/left -b nice_nano -- -DSHIELD=kyria_left -DZMK_CONFIG=$config_dir
printf "Building Right"
printf '=%.0s' {1..30}
printf "\n"
west build -d build/right -b nice_nano -- -DSHIELD=kyria_right -DZMK_CONFIG=$config_dir


printf "Moving Artifacts"
printf '+%.0s' {1..30}
printf "\n"
today=$(date +%Y-%m-%d)
dest_folder="../$today"
dest_folder=$(realpath $dest_folder)
echo "Destintation Folder: $dest_folder"
mkdir -p $dest_folder
left_path="$dest_folder/kyria_left.uf2"
right_path="$dest_folder/kyria_right.uf2"
cp build/left/zephyr/zmk.uf2 $left_path 
cp build/right/zephyr/zmk.uf2 $right_path
# cp $config_dir "$dest_folder/" # mount config_dir in container for this feature
# docker volume create --driver local -o o=bind -o type=none -o \
#    device="/full/path/to/your/zmk-config/" zmk-config
echo "Done"
echo "$left_path"
echo "$right_path"



