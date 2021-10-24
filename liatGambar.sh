echo Menunjukkan gambar pada topic /camera/color/image_raw
echo 1./camera/color/image_raw
echo 2./camera/depth/image_rect_raw
echo 3./camera/depth/image_rect_raw/compressed
echo 4./camera/depth/image_rect_raw/theora
echo \n
echo Topic yang mana yang akan anda lihat?:
read -p "Masukkan angka:" varOption

case $varOption in
    1)
        echo Viewing /camera/color/image_raw
        rostopic type /camera/color/image_raw
        rosrun image_view image_view image:=/camera/color/image_raw;;
    2)
        echo Viewing /camera/depth/image_rect_raw
        rostopic type /camera/depth/image_rect_raw
        rosrun image_view image_view image:=/camera/depth/image_rect_raw;;
    *)
        echo Sorry not coded yet;;
esac
# if [ $varOption="1" ]
# then
#     echo Viewing /camera/color/image_raw
#     # rosrun image_view image_view image:=/camera/color/image_raw

# elif [ $varOption="2" ]
# then
#     echo Viewing /camera/depth/image_rect_raw
#     # rosrun image_view image_view image:=/camera/depth/image_rect_raw
# else
#     echo Sorry not coded yet hehe :3
# fi