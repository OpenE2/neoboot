#!/bin/sh
#script - gutosie
if `grep -q 'osd.language=pl_PL' </etc/enigma2/settings`; then
  PL=1
fi

if [ -f /proc/stb/info/vumodel ];  then  
    VUMODEL=$( cat /proc/stb/info/vumodel )     
fi 

if [ -f /proc/stb/info/boxtype ];  then  
    BOXTYPE=$( cat /proc/stb/info/boxtype )    
fi

if [ -f /proc/stb/info/chipset ];  then  
    CHIPSET=$( cat /proc/stb/info/chipset )    
fi

if [ -f /tmp/zImage.ipk ];  then  
    rm -f /tmp/zImage.ipk    
fi

if [ -f /tmp/zImage ];  then  
    rm -f /tmp/zImage    
fi

KERNEL=`uname -r` 
IMAGE=ImageBoot
IMAGENEXTBOOT=/ImageBoot/.neonextboot
NEOBOOTMOUNT=$( cat /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location) 
BOXHOSTNAME=$( cat /etc/hostname)
UPLOAD=ImagesUpload
NandWrite=/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot//bin/nandwrite

if [ -f $NEOBOOTMOUNT$IMAGENEXTBOOT ]; then
  TARGET=`cat $NEOBOOTMOUNT$IMAGENEXTBOOT`
else
  TARGET=Flash              
fi
                   
if [ $VUMODEL = "bm750" ] || [ $BOXHOSTNAME = "vuduo" ] || [ $BOXHOSTNAME = "vusolo" ] || [ $BOXHOSTNAME = "vuuno" ] || [ $BOXHOSTNAME = "vuultimo" ]; then
    if [ -f /proc/stb/info/vumodel ] || [ ! -e /proc/stb/info/boxtype ] ; then
        if [ $TARGET = "Flash" ]; then                    
                if [ -e /.multinfo ]; then                                                
                            if [ -f /proc/stb/info/vumodel ] || [ ! -e /proc/stb/info/boxtype ]; then
                                if [ -e $NEOBOOTMOUNT$UPLOAD/.kernel/$BOXHOSTNAME.vmlinux.gz ] ; then
                                    [ $PL ] && echo "Kasowanie kernel z /dev/mtd1..." || echo "Erase kernel from  /dev/mtd1"
                                    sleep 2                                
                                    flash_eraseall /dev/mtd1 > /dev/null 2>&1
                                    [ $PL ] && echo "Wgrywanie kernel do /dev/mtd1..." || echo "Writing kernel to from  /dev/mtd1"  
                                    sleep 2
                                    $NandWrite -p /dev/mtd1 $NEOBOOTMOUNT$UPLOAD/.kernel/$BOXHOSTNAME.vmlinux.gz > /dev/null 2>&1
                                fi
                            fi
                            update-alternatives --remove vmlinux vmlinux-`uname -r` || true                                          
                            echo "NEOBOOT is booting image " $TARGET
                            echo "Used Kernel: " $TARGET > $NEOBOOTMOUNT$UPLOAD/.kernel/used_flash_kernel                           

                elif [ ! -e /.multinfo ]; then
                            if [ -f /proc/stb/info/vumodel ] || [ ! -e /proc/stb/info/boxtype ]; then 
                                if [ $VUMODEL = "bm750" ] || [ $VUMODEL = "duo" ] || [ $VUMODEL = "solo" ] || [ $VUMODEL = "uno" ] || [ $VUMODEL = "ultimo" ]; then                    
                                    if [ -e $NEOBOOTMOUNT$UPLOAD/.kernel/$BOXHOSTNAME.vmlinux.gz ] ; then
                                        [ $PL ] && echo "Kasowanie kernel z /dev/mtd1..." || echo "Erase kernel from  /dev/mtd1"                                   
                                        sleep 2
                                        flash_eraseall /dev/mtd1 > /dev/null 2>&1
                                        [ $PL ] && echo "Wgrywanie kernel do /dev/mtd1..." || echo "Writing kernel to from  /dev/mtd1"                                           
                                        sleep 2
                                        $NandWrite -p /dev/mtd1 $NEOBOOTMOUNT$UPLOAD/.kernel/$BOXHOSTNAME.vmlinux.gz > /dev/null 2>&1
                                    fi
                                fi
                            fi    
                            update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                            echo "NEOBOOT is booting image " $TARGET
                            echo "Used Kernel: " $TARGET > $NEOBOOTMOUNT$UPLOAD/.kernel/used_flash_kernel
                fi
                echo "...............Shutdown Now..............."
                sync && echo 3 > /proc/sys/vm/drop_caches
                sleep 10
                PATH=/sbin:/bin:/usr/sbin:/usr/bin 
                reboot -d -f 
        else                  	    
                        if [ -e /.multinfo ] ; then
                                INFOBOOT=$( cat /.multinfo )
                                if [ $TARGET = $INFOBOOT ] ; then
                                    echo "NEOBOOT is booting image from " $TARGET                                    
                                else                                    
                                    [ $PL ] && echo "Kasowanie kernel z /dev/mtd1..." || echo "Erase kernel from  /dev/mtd1"                                   
                                    sleep 2
                                    flash_eraseall /dev/mtd1 > /dev/null 2>&1
                                    [ $PL ] && echo "Wgrywanie kernel do /dev/mtd1..." || echo "Writing kernel to from  /dev/mtd1"                                                                      
                                    sleep 2
                                    $NandWrite -p /dev/mtd1 $NEOBOOTMOUNT$IMAGE/$TARGET/boot/$BOXHOSTNAME.vmlinux.gz > /dev/null 2>&1  
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "NEOBOOT is booting image" $TARGET
                                    echo "Used Kernel: " $TARGET   > $NEOBOOTMOUNT$UPLOAD/.kernel/used_flash_kernel
                                fi
                        else
                                    [ $PL ] && echo "Kasowanie kernel z /dev/mtd1..." || echo "Erase kernel from  /dev/mtd1"                                   
                                    sleep 2
                                    flash_eraseall /dev/mtd1 > /dev/null 2>&1 
                                    [ $PL ] && echo "Wgrywanie kernel do /dev/mtd1..." || echo "Writing kernel to from  /dev/mtd1"
                                    sleep 2
                                    $NandWrite -p /dev/mtd1 $NEOBOOTMOUNT$IMAGE/$TARGET/boot/$BOXHOSTNAME.vmlinux.gz > /dev/null 2>&1                                                                                                     
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "NEOBOOT is booting image " $TARGET
                                    echo "Used Kernel: " $TARGET   > $NEOBOOTMOUNT$UPLOAD/.kernel/used_flash_kernel                                       
                        fi                
                        echo "...............Shutdown Now..............." 
                        sync && echo 3 > /proc/sys/vm/drop_caches
                        sleep 5
                        PATH=/sbin:/bin:/usr/sbin:/usr/bin 
                        reboot -d -f
        fi
    fi        
else
                    ln -sfn /sbin/init.sysvinit /sbin/init
                    echo "CHIPSET: " $CHIPSET " BOX NAME: "$BOXHOSTNAME" MODEL: "$VUMODEL" "
                    echo "$TARGET "  > $NEOBOOTMOUNT/ImageBoot/.neonextboot
                    [ $PL ] && echo "Ten model stb nie jest wpierany" || echo "This stb model is not supported." 
                    [ $PL ] && echo "Wspierane modele: vuduo, vusolo, vuuno, vuultimo" || echo "Supported model: vuduo, vusolo, vuuno, vuultimo "                     
                    exit 0
fi
exit 0

