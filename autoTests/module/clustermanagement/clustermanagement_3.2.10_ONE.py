#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.2.10.py - test case 3.2.10 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-18 17:44:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.2.10 AC间二层自动发现(IPV6)
# 测试目的：测试AC间二层自动发现功能是否正常(IPV6)
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.2.10'

avoiderror(testname)
printTimer(testname,'Start','Test two layer automatic discovery between AC')

################################################################################
#Step 1
#
#操作
#关闭AC1三层发现功能
#关闭AC2二层和三层发现功能
#
#预期
#AC1上show wireless peer-switch显示“No peer wireless switch exists”
################################################################################

printStep(testname,'Step 1',
          'Close the ip list discovery',
          'Check the result')

# operate
exec(compile(open('clustermanagement\\clustermanagement_initial(ipv6).py', "rb").read(), 'clustermanagement\\clustermanagement_initial(ipv6).py', 'exec'))

EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery method ip-poll')
SetCmd(switch1,'no discovery vlan-list 1')
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

EnterWirelessMode(switch2)
SetCmd(switch2,'no discovery method ip-poll')
	
IdleAfter(30)
#check
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
				   check=[('No peer wireless switch exists')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
#把vlan70加入到AC1的二层发现vlan list中
#
#预期
#AC1上show wireless discovery vlan-list看到vlan发现列表“VLAN”中有“vlan70”
################################################################################

printStep(testname,'Step 2',
          'Add management vlan to discovery vlan list on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery vlan-list',Vlan70)

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless discovery vlan-list')
#check
res1 = CheckLine(data1,'70','Vlan0070',IC=True)
	
#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
# 等待30s后,在AC1上查看peer AC
#
#预期
# AC1上show wireless peer-switch显示“No peer wireless switch exists”
################################################################################

printStep(testname,'Step 3',
          'Check peer switch status on AC1',
		  'Check the result')		  

# operate		  
IdleAfter(30)
#check
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
				   check=[('No peer wireless switch exists')],
				   retry=30,interval=5,waitflag=False,IC=True)
				  						
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
#修改vlan70的接口IP为IF_VLAN70_S1_BACKIPV6,使IF_VLAN70_S1_BACKIPV6>IF_VLAN70_S2_IPV6
#
#预期
#AC1上show wireless peer-switch显示“No peer wireless switch exists”
################################################################################

printStep(testname,'Step 4',
          'Change AC1 ip index greater then AC2 ip index',
          'Check the result')

# operate		  
EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan70)
SetCmd(switch1,'no ipv6 address',If_vlan70_s1_ipv6)
SetCmd(switch1,'ipv6 address',If_vlan70_s1_backipv6)
SetCmd(switch1,'exit')

EnterWirelessMode(switch1)
SetCmd(switch1,'static-ipv6',If_vlan70_s1_backipv6_s)
SetCmd(switch1,'exit')

IdleAfter(30)
#check
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
				   check=[('No peer wireless switch exists')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#把vlan70加入到AC2的二层发现vlan list中
#
#预期
#AC2上show wireless discovery vlan-list看到vlan发现列表“VLAN”中有“vlan70”
################################################################################

printStep(testname,'Step 5',
          'Add management vlan to discovery vlan list on AC2',
          'Check the result')

# operate
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery vlan-list',Vlan70)

EnterEnableMode(switch2)
data1 = SetCmd(switch2,'show wireless discovery vlan-list')

#check
res1 = CheckLine(data1,'70','VLAN0070',IC=True)

#result
printCheckStep(testname,'Step 5', res1)

################################################################################
#Step 6
#
#操作
#在AC1上查看peer AC
#
#预期
#AC1上show wireless peer-switch显示有:
#“IP Address”为“IF_VLAN70_S2_IPV6_s”的,“Disc. Reason”显示为“L2 Poll”
################################################################################

printStep(testname,'Step 6',
          'Check peer switch status on AC1 2',
          'Check the result')

# operate
IdleAfter(30)
#check
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
				   check=[('L2 Poll'),(If_vlan70_s2_ipv6_s)],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname,'Step 6', res1)

################################################################################
#Step 7
#
#操作
#在AC2上把s2p1接口down掉
#
#预期
#在AC1上show wireless peer-switch显示“No peer wireless switch exists”
################################################################################

printStep(testname,'Step 7',
          'Shutdown the interface on AC2',
          'Check the result')

# operate
EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'shutdown')

IdleAfter(30)
#check
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
				   check=[('No peer wireless switch exists')],
				   retry=30,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname,'Step 7', res1)

################################################################################
#Step 8
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 8',
          'Recover initial config')

# operate		  
#恢复AC1的配置
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery method ip-poll')
SetCmd(switch1,'no discovery vlan-list',Vlan70)
SetCmd(switch1,'discovery vlan-list 1')
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

#恢复AC2的配置
EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'no shutdown')
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery method ip-poll')
SetCmd(switch2,'discovery method l2-multicast')
SetCmd(switch2,'no discovery vlan-list',Vlan70)

#AC1操作
# EnterConfigMode(switch1)
# SetCmd(switch1,'interface vlan',Vlan70)
# SetCmd(switch1,'ipv6 address',If_vlan70_s1_ipv6)
# SetCmd(switch1,'no ipv6 address',If_vlan70_s1_backipv6)

# EnterWirelessMode(switch1)
# SetCmd(switch1,'static-ipv6',If_vlan70_s1_ipv6_s)

exec(compile(open('clustermanagement\\clustermanagement_unitial(ipv6).py', "rb").read(), 'clustermanagement\\clustermanagement_unitial(ipv6).py', 'exec'))	  
#end
printTimer(testname, 'End')