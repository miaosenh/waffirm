#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apwds_1.3.10.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 1.3.10	Open方式下,satelliteap的vap0与rootap的vapx建立wds
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.25
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase apwds_1.3.10'
avoiderror(testname)
printTimer(testname,'Start','Use vap0 of satelliteap and vapx of rootap to establish wds link')
###############################################################################
#Step 1
#操作
# AP2上进行open模式的WDS配置
# set wds wds0 wds-mode satelliteap
# set wds wds0 wds-ssid ${wds_ssid}    
# set wds wds0 remote-mac ap1mac_network2   
# set wds wds0 wds-security-policy plain-text    
# set wds wds0 wds-status up
# AC上在network2 配置wds并下发给ap1
# network 2   
# wds-mode rootap    
# security mode none    
# wds-remote-vap ap2mac 
# ssid ${wds_ssid}
#预期
# 配置成功
################################################################################
printStep(testname,'Step 1','AP2 config wds0 as open mode',\
                    'Config wds in network 2 on AC1',\
                    'Apply ap profile 1')
res1=1
#operate
# AP2上配置wds0,mode为satelliteap
Ap_openwds_config(ap2,Ap2cmdtype,
                    wds0num,
                    ssid=wds_ssid,
                    remotemac=ap1mac_type1_network2)
# AC上配置network2为wds，apmode为rootap，并下发profile 1
Ac_wds_config(switch1,2,
                ssid=wds_ssid,
                remotemac=ap2vapmac)
res1=WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#操作
#检查AC1是否成功管理AP2,WDS连接是否建立
#预期
#AC1 上show wireless ap status可以看到AP2被成功管理
# AC1上show wireless wds link status可以看到AP1和AP2建立起wds连接
################################################################################

printStep(testname,'Step 2',\
                    'Check WDS is linked and AC1 managed ap2 successfully')
res1=res2=1
#operate
res1 = CheckSutCmd(switch1,'show wireless ap status', \
                    check=[(ap2mac,'Managed','Success')], \
                    retry=40,interval=5,waitflag=False,IC=True)
res2 = CheckSutCmd(switch1,'show wireless wds link status', \
                    check=[(ap1mac,radionum,'1',ap2mac,radionum,'0','Managed','Managed','Connected')], \
                    waittime=5,retry=5,interval=1,IC=True)                    
#result
printCheckStep(testname, 'Step 2',res1,res2)

################################################################################
#Step 3
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 3',\
          'Recover initial config for switches.')

#operate
# 恢复network2配置
ClearNetworkConfig(switch1,2)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# 恢复AP2初始化配置
RebootAp(connectTime=1,setdefaut=True,AP=ap2,apcmdtype=Ap2cmdtype)
Initial_ap2()
#end
printTimer(testname, 'End')