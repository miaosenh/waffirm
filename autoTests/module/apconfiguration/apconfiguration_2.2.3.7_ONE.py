#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.3.7_ONE.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features: 
# 2.2.3.7-9	Controller上可以按ap-group升级(合并用例2.2.3.7,2.2.3.8,2.2.3.9)
# 测试目的： 
# 2.2.3.7 Controller上可以wireless ap download start ap-group <word>触发手动独立升级此ap-group的所有ap，自己管理ap重启后被AC管理，image版本已经更新成功。
# 2.2.3.8 Controller上可以wireless ap download start ap-group <word>触发手动独立升级此ap-group的所有ap，peer上ap重启后被AC管理，image版本已经更新成功。
# 2.2.3.9 Controller上可以wireless ap download start ap-group <word>触发手动独立升级此ap-group的所有ap，其它ap-group的ap不会被触发。
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.3.30
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'apconfiguration_2.2.3.7-9'
avoiderror(testname)
printTimer(testname,'Start','Controller  upgrade ap-group(classfied by name)')
###############################################################################
#Step 1
#操作
# 在AC1上配置discovery ip-list StaticIpv4_ac2
# 在AP2上配置管理AC的地址为AC2的IP
# set managed-ap switch-address-1 ac2_ip
# 重启AP2
# 预期
# AC1和AC2建立集群关系
# AP2被AC2成功管理
################################################################################
printStep(testname,'Step 1',
          'config discovery ip-list StaticIpv4_ac2 on ac1',
          'ap2 set managed-ap switch-address-1 ac2_ip',
          'reboot ap2',
          'ac1 and ac2 are in a cluster',
          'ac2 manages ap2 successfully')
res1=res2=1
#operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'cluster-priority 10')
SetCmd(switch1,'discovery ip-list',StaticIpv4_ac2)

# AP2上配置管理AC的地址为AC2的IP
ApSetcmd(ap2,Ap2cmdtype,'set_switch_address',StaticIpv4_ac2,addressnum='1')
ApSetcmd(ap2,Ap2cmdtype,'saverunning')
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap2, ap2mac, switch1, Ap2cmdtype)
IdleAfter(30)

# 检查AC1和AC2建立集群关系
res1=CheckSutCmd(switch1,'show wireless peer-switch', 
                 check=[(StaticIpv4_ac2)],
                 retry=20,interval=5,waitflag=False,IC=True)
# 检查AP2是否被AC2管理
res2=CheckSutCmd(switch2,'show wireless ap status', 
                 check=[(ap2mac,'Managed','Success')],
                 retry=20,interval=10,waitflag=False,IC=True)
#result
printCheckStep(testname, 'Step 1',res1,res2)
###############################################################################
#Step 2
#操作
# 在AC1上为AP1_image_type指定image文件为ap1_standby_build，
# 在AC1上为AP2_image_type指定image文件为ap2_standby_build，
# 将AP1加入ap-group 111中，升级ap-group 111
# 预期
# AP1升级成功
# AP2没有升级
################################################################################
printStep(testname,'Step 2',
          'controller config ap1_image_type upgrade to ap1_standby_build',
          'controller config ap2_image_type upgrade to ap2_standby_build',
          'add ap1mac to group 111',
          'controller upgrade group 111'
          'ap1 upgrade successfully',
          'ap2 should not upgrade')

#operate
# 查看AP2当前的版本号
ap2_version = Get_ap_version(ap2, Ap2cmdtype)

# 在AC1上为AP1和AP2指定image文件
# (脚本中先配置AP2再配置AP1，目的是如果AP2和AP1的image type相同时，AP2的配置会被AP1覆盖）
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap2_image_type, ap2_ftpupgrade_standby_path)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, ap1_ftpupgrade_standby_path)

# 创建group 111,将AP1加入group 111
EnterWirelessMode(switch1)
SetCmd(switch1,'ap-group 111')
SetCmd(switch1,'permit-ap-name', ap1mac)

# 升级group 111组内所有AP
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap download start ap-group 111')

# 等待升级完成
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)

# check
# 检查AC1是否重新管理AP1和AP2
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                 retry=20,interval=5,waitflag=False,IC=True)
# 检查AP1升级成功
ApLogin(ap1)
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_standby_buildnum)
# 检查AP2没有升级 
res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_version)
#result
printCheckStep(testname, 'Step 2',res1,res2,res3)
###############################################################################
#Step 3
#操作
# 将AP2加入ap-group 111中，将AP1删除，升级ap-group 111
# 预期
# AP2升级成功
################################################################################
printStep(testname,'Step 3',
          'add ap2mac to group 111 and delete ap1mac',
          'controller upgrade group 111'
          'ap2 upgrade successfully')

#operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap2_image_type, ap2_ftpupgrade_standby_path)

EnterWirelessMode(switch1)
SetCmd(switch1,'no ap-group 111')
SetCmd(switch1,'ap-group 111')
SetCmd(switch1,'permit-ap-name', ap2mac)

# 升级group 111组内所有AP
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap download start ap-group 111')

# 等待升级完成
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)

# check
# 检查AC1是否重新管理AP1和AP2
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                 retry=20,interval=5,waitflag=False,IC=True)
# 检查AP2升级成功
ApLogin(ap2)
res2 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_standby_buildnum)

#result
printCheckStep(testname, 'Step 2',res1,res2)
###############################################################################
#Step 3
#操作
# 在AC1上为AP1_image_type指定image文件为ap1_current_build，
# 在AC1上为AP2_image_type指定image文件为ap2_current_build，
# 将AP1和AP2加入ap-group 111，升级ap-group 111
# 预期
# AP1和AP2升级成功
################################################################################
printStep(testname,'Step 3',
          'controller config ap1_image_type upgrade to ap1_standby_build',
          'controller config ap2_image_type upgrade to ap2_standby_build',
          'add ap1mac and ap2mac to ap-group 111',
          'upgrade group 111'
          'ap1 and ap2 upgrade successfully')

#operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap2_image_type, ap2_ftpupgrade_current_path)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, ap1_ftpupgrade_current_path)

EnterWirelessMode(switch1)
SetCmd(switch1,'ap-group 111')
SetCmd(switch1,'permit-ap-name', ap1mac)
SetCmd(switch1,'permit-ap-name', ap2mac)

# 升级group 111组内所有AP
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap download start ap-group 111')

# 等待升级完成
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)

# check
res1 = CheckSutCmd(switch1,'show wireless ap status', 
                   check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                   retry=20,interval=5,waitflag=False,IC=True)
# 检查AP1和AP2升级成功
ApLogin(ap1)
ApLogin(ap2)
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_current_buildnum)
if ap1_image_type == ap2_image_type:
    ApLogin(ap2)
    res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap1_current_buildnum)
else:
    res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_current_buildnum)
#result
printCheckStep(testname, 'Step 2',res1,res2,res3)
################################################################################
# Step 4
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 4',
          'Recover initial config')
          
# 恢复AP2配置
ApSetcmd(ap2,Ap2cmdtype,'set_switch_address',StaticIpv4_ac1,addressnum='1')
ApSetcmd(ap2,Ap2cmdtype,'saverunning')
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap2, ap2mac, switch2, Ap2cmdtype)
# 恢复AC1配置
EnterWirelessMode(switch1)
SetCmd(switch1, 'no wireless ap download image-type',ap1_image_type)
SetCmd(switch1, 'no wireless ap download image-type',ap2_image_type)
SetCmd(switch1, 'no ap-group 111')
SetCmd(switch1, 'no cluster-priority')
SetCmd(switch1, 'no discovery ip-list',StaticIpv4_ac2)
SetCmd(switch1, 'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
IdleAfter(30)
CheckSutCmd(switch1,'show wireless peer-switch', 
            check=[('No peer wireless switch exists')],
            retry=10,interval=5,waitflag=False,IC=True)

CheckSutCmd(switch2,'show wireless ap status', 
            check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
            retry=20,interval=10,waitflag=False,IC=True)
#end
printTimer(testname, 'End')