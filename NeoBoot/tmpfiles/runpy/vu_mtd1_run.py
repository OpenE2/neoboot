# -*- coding: utf-8 -*-
 
from Plugins.Extensions.NeoBoot.__init__ import _                                                                                                                                                   
from Plugins.Extensions.NeoBoot.files.stbbranding import getNeoLocation, getCPUtype, getCPUSoC,  getImageNeoBoot, getBoxVuModel, getBoxHostName, getNeoMount, getNeoMount2,getNeoMount3, getNeoMount4, getNeoMount5
from enigma import getDesktop
from enigma import eTimer
from Screens.Screen import Screen                                                                                                                                               
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Screens.Standby import TryQuitMainloop
from Components.About import about
from Components.Sources.List import List
from Components.Button import Button
from Components.ActionMap import ActionMap, NumberActionMap
from Components.GUIComponent import *
from Components.MenuList import MenuList
from Components.Input import Input
from Components.Label import Label
from Components.ProgressBar import ProgressBar
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap, MultiPixmap
from Components.config import *
from Components.ConfigList import ConfigListScreen
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, pathExists, createDir, resolveFilename, SCOPE_PLUGINS
from os import system, listdir, mkdir, chdir, getcwd, rename as os_rename, remove as os_remove, popen
from os.path import dirname, isdir, isdir as os_isdir
import os
import time                 
LinkNeoBoot = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'


class StartImage(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = """<screen position="center, center" size="1241, 850" title="NeoBoot">
        \n\t\t\t<ePixmap position="491, 673" zPosition="-2" size="365, 160" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrixhd.png" />
        <widget source="list" render="Listbox" position="20, 171" size="1194, 290" scrollbarMode="showOnDemand">\n\t\t\t\t<convert type="TemplatedMultiContent">
        \n                \t\t{"template": [
        \n                    \t\t\tMultiContentEntryText(pos = (90, 1), size = (920, 66), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
        \n                    \t\t\tMultiContentEntryPixmapAlphaTest(pos = (8, 4), size = (66, 66), png = 1),
        \n                    \t\t\t],
        \n                    \t\t\t"fonts": [gFont("Regular", 40)],\n                    \t\t\t"itemHeight": 66\n                \t\t}
        \n            \t\t</convert>\n\t\t</widget>
        \n         <widget name="label1" position="21, 29" zPosition="1" size="1184, 116" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
        \n\t\t        <widget name="label2" position="22, 480" zPosition="-2" size="1205, 168" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
        \n\t\t        </screen>"""
    else:
        skin = """<screen position="center, center" size="835, 500" title="NeoBoot">
        \n\t\t\t           <ePixmap position="0,0" zPosition="-1" size="835,500" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/frame835x500.png"  />
        <widget source="list" render="Listbox" position="16, 150" size="800, 40"    selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/listselection800x35.png" scrollbarMode="showOnDemand">
        \n\t\t\t\t<convert type="TemplatedMultiContent">
        \n                \t\t{"template": [
        \n                    \t\t\tMultiContentEntryText(pos = (180, 0), size = (520, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
        \n                    \t\t\tMultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (36, 36), png = 1),
        \n                    \t\t\t],\n                    \t\t\t"fonts": [gFont("Regular", 22)],
        \n                    \t\t\t"itemHeight": 35\n               \t\t}\n            \t\t</convert>
        \n\t\t</widget>\n<widget name="label1" font="Regular; 26" position="15, 70" size="803, 58" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00cc99" />
        <widget name="label2" position="40, 232" zPosition="2" size="806, 294" font="Regular;25" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00cc99" />
        \n\t\t        </screen>"""

    __module__ = __name__
    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.select()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close})
        self['label1'] = Label(_('Start the chosen system now ?'))
        self['label2'] = Label(_('Select OK to run the image.'))
        
    def select(self):
        self.list = []
        mypath = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'
        if not fileExists(mypath + 'icons'):
            mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/ok.png'
        png = LoadPixmap(mypixmap)
        res = (_('OK Start image...'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self): 
        if getImageNeoBoot() != 'Flash': 
                os.system('rm -rf %sImageBoot/%s/usr/bin/enigma2_pre_start.sh' % ( getNeoLocation(), getImageNeoBoot())) 
                self.StartImageInNeoBoot()
        else:
            os.system('rm -rf %sImageBoot/%s/usr/bin/enigma2_pre_start.sh' % ( getNeoLocation(), getImageNeoBoot())) 
            self.StartImageInNeoBoot()
        #---------------------------------------------
        os.system('touch ' + LinkNeoBoot + '/files/mountpoint.sh; echo "#!/bin/sh\n#DESCRIPTION=This script by gutosie\n"  > ' + LinkNeoBoot + '/files/mountpoint.sh; chmod 0755 ' + LinkNeoBoot + '/files/mountpoint.sh') 
        if getNeoMount() == 'hdd_install_/dev/sda1': 
                    os.system('echo "umount -l /media/hdd\nmkdir -p /media/hdd\n/bin/mount /dev/sda1 /media/hdd"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
        elif getNeoMount() == 'hdd_install_/dev/sdb1': 
                    os.system('echo "umount -l /media/hdd\nmkdir -p /media/hdd\n/bin/mount /dev/sdb1 /media/hdd"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
        elif getNeoMount() == 'hdd_install_/dev/sda2': 
                    os.system('echo "umount -l /media/hdd\nmkdir -p /media/hdd\n/bin/mount /dev/sda2 /media/hdd"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
        elif getNeoMount() == 'hdd_install_/dev/sdb2': 
                    os.system('echo "umount -l /media/hdd\nmkdir -p /media/hdd\n/bin/mount /dev/sda2 /media/hdd"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
        #---------------------------------------------
        if getNeoMount2() == 'usb_install_/dev/sdb1': 
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sdb1 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')      
        elif getNeoMount2() == 'usb_install_/dev/sda1': 
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sda1 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')  
        elif getNeoMount2() == 'usb_install_/dev/sdb2': 
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sdb2 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')  
        elif getNeoMount2() == 'usb_install_/dev/sdc1': 
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sdc1 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')  
        elif getNeoMount2() == 'usb_install_/dev/sdd1': 
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sdd1 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')  
        elif getNeoMount2() == 'usb_install_/dev/sde1': 
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sde1 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')  
        elif getNeoMount2() == 'usb_install_/dev/sdf1': 
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sdf1 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')  
        #---------------------------------------------                                  
        elif getNeoMount3() == 'cf_install_/dev/sda1': 
                    os.system('echo "umount -l /media/cf\nmkdir -p /media/cf\n/bin/mount /dev/sda1 /media/cf"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
        elif getNeoMount3() == 'cf_install_/dev/sdb1': 
                    os.system('echo "umount -l /media/cf\nmkdir -p /media/cf\n/bin/mount /dev/sdb1 /media/cf"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
        #---------------------------------------------
        elif getNeoMount4() == 'card_install_/dev/sda1': 
                    os.system('echo "umount -l /media/card\nmkdir -p /media/card\n/bin/mount /dev/sda1 /media/card"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
        elif getNeoMount4() == 'card_install_/dev/sdb1': 
                    os.system('echo "umount -l /media/card\nmkdir -p /media/card\n/bin/mount /dev/sdb1 /media/card"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
        #---------------------------------------------
        elif getNeoMount5() == 'mmc_install_/dev/sda1': 
                    os.system('echo "umount -l /media/mmc\nmkdir -p /media/mmc\n/bin/mount /dev/sda1 /media/mmc"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
        elif getNeoMount5() == 'mmc_install_/dev/sdb1': 
                    os.system('echo "umount -l /media/mmc\nmkdir -p /media/mmc\n/bin/mount /dev/sdb1 /media/mmc"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
        os.system('echo "\n\nexit 0"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')

    def StartImageInNeoBoot(self):                              
        if getImageNeoBoot() != 'Flash':
            if fileExists('%sImageBoot/%s/.control_ok' % ( getNeoLocation(),  getImageNeoBoot())): 
                system('touch /tmp/.control_ok ') 
            else:
                system('touch %sImageBoot/%s/.control_boot_new_image ' % ( getNeoLocation(), getImageNeoBoot() ))

        system('chmod 755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/kernel.sh')                                                  
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]     
        if self.sel == 0:          
            if fileExists('/media/InternalFlash/etc/init.d/neobootmount.sh'):
                os.system('rm -f /media/InternalFlash/etc/init.d/neobootmount.sh;')
                
            #VUPLUS MIPS vu_dev_mtd1.sh   
            if getBoxHostName() == 'vuultimo' or getBoxHostName() == 'bm750' or getBoxHostName() == 'vuduo' or getBoxHostName() == 'vuuno' or getBoxHostName() == 'vusolo' or getBoxHostName() == 'vuduo':                              
                        if not fileExists('%sImagesUpload/.kernel/%s.vmlinux.gz' % (getNeoLocation(), getBoxHostName()) ):
                            self.myclose2(_('Error - in the location %sImagesUpload/.kernel/ \nkernel file not found flash kernel vmlinux.gz ' % getNeoLocation() ))                                                                              
                        else:                        
                            if getImageNeoBoot() == 'Flash':                    
                                if fileExists('/.multinfo'): 
                                    cmd = "echo -e '\n\n%s '" % _('...............NeoBoot  REBOOT...............\nPlease wait, in a moment the decoder will be restarted...')                                                                                                       
                                    cmd1 = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/kernel.sh'                  
                                elif not fileExists('/.multinfo'):
                                    cmd = "echo -e '\n\n%s '" % _('...............NEOBOOT >> Reboot...............\nPlease wait, in a moment the decoder will be restarted...')                                                                      
                                    cmd1 = 'ln -sfn /sbin/init.sysvinit /sbin/init; /etc/init.d/reboot'

                            elif getImageNeoBoot() != 'Flash':                       
                                if not fileExists('/.multinfo'):                        

                                    if fileExists('' + getNeoLocation() + 'ImageBoot/' + getImageNeoBoot() + '/boot/' + getBoxHostName() + '.vmlinux.gz'):
                                        cmd = "echo -e '\n\n%s '" % _('...............NEOBOOT-REBOOT...............\nPlease wait, in a moment the decoder will be restarted...') 
                                        cmd1 = 'ln -sfn /sbin/neoinitmipsvu /sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/kernel.sh'  

                                    elif not fileExists('%sImageBoot/%s/boot/%s.vmlinux.gz' % ( getNeoLocation(), getImageNeoBoot(), getBoxHostName())):
                                        cmd = "echo -e '\n\n%s '" % _('...............NEOBOOT > REBOOT...............\nPlease wait, in a moment the decoder will be restarted...')                                    
                                        cmd1 = 'ln -sfn /sbin/neoinitmipsvu /sbin/init; /etc/init.d/reboot'                                                                                 

                                elif fileExists('/.multinfo'):    
                                    if not fileExists('%sImageBoot/%s/boot/%s.vmlinux.gz' % ( getNeoLocation(), getImageNeoBoot(), getBoxHostName())):
                                        cmd = "echo -e '\n\n%s '" % _('...............NEOBOOT_REBOOT...............\nPlease wait, in a moment the decoder will be restarted...')                                    
                                        cmd1 = 'flash_eraseall /dev/mtd1; sleep 2; ' +LinkNeoBoot+ '/bin/nandwrite -p /dev/mtd1 %sImagesUpload/.kernel/%s.vmlinux.gz; /etc/init.d/reboot' % getNeoLocation(), getBoxHostName()

                                    elif fileExists('%sImageBoot/%s/boot/%s.vmlinux.gz' % ( getNeoLocation(), getImageNeoBoot(), getBoxHostName())):
                                        cmd = "echo -e '\n\n%s '" % _('...............REBOOT now...............\nPlease wait, in a moment the decoder will be restarted...')                                    
                                        cmd1 = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/kernel.sh'

                            self.session.open(Console, _('NeoBoot MIPS....'), [cmd, cmd1])
                            self.close()

            else:
                            os.system('echo "Flash "  >> ' + getNeoLocation() + 'ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('It looks like it that multiboot does not support this STB.'), MessageBox.TYPE_INFO, 8)
                            self.close()

    def myclose2(self, message):
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        self.close()
