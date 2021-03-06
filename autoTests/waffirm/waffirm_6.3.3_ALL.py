#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_6.3.3.py - test case 6.3.3 of waffirm
#
# Author: 
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 6.3.3 management vlan 和untag vlan不相同情况下超长重定向url的外置Portal功能测试
# 测试目的：测试management vlan 和untag vlan不相同情况下的超长重定向url的外置portal 认证测试
# 测试环境：同测试拓扑
# 测试描述：测试ap management vlan 和untag vlan不相同情况下客户端发起HTTP请求时，能够成功重定向到超长外置Portal的认证页面，客户端能够成功的上/下线
#          （STA1的MAC地址：STA1MAC）
#
#*******************************************************************************
# Change log:
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 6.3.3'
avoiderror(testname)
printTimer(testname,'Start','Test extrnal portal')

###############################################################################
#Step 1
#操作
#在AC1配置network1的SSID为test1，关联vlan4091，配置下发到AP1，
#配置Radius服务器
#配置外置Portal
#
#
#预期
#配置成功
################################################################################
printStep(testname,'Step 1',
          'set radius server-name acct wlan,',
          'set radius setver-name auth wlan,',
          'and u should config others and so on,',
          'check config success,'
          'config captive-portal,')

Network_name4='12345678901234567890123456789012'
# SetCmd(ap1,'set management vlan-id',Vlan20)
# SetCmd(ap1,'set untagged-vlan vlan-id 2')
# ApSetcmd(ap1,Ap1cmdtype,'set_management_vlanid',Vlan20)
# ApSetcmd(ap1,Ap1cmdtype,'set_untagged_vlanid','2',commitflag=True)

EnterNetworkMode(switch1,1)
SetCmd(switch1,'ssid ' + Network_name4)
SetCmd(switch1,'vlan ' + Vlan4091)
# AC修改management vlan和ethernet native-vlan配置，并下发profile
EnterWirelessMode(switch1)
EnterApProMode(switch1,'1')
SetCmd(switch1,'management vlan',Vlan20)
SetCmd(switch1,'ethernet native-vlan 2')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# 配置下发后，ap的management vlan和ethernet native-vlan已经修改，
# 但是s3的端口配置没有修改，导致AP和AC之间不通，AP会下线
# （注意：此处必须先等AP下线后再修改S3配置）
CheckSutCmd(switch1,'show wireless ap status',
            check=[(ap1mac,'Failed','Not Config')],
            waitflag=False,retry=10,interval=5,IC=True)


# 修改S3端口配置
EnterConfigMode(switch3)
SetCmd(switch3,'vlan 2')
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan 2')

IdleAfter(20)
res1=CheckSutCmd(switch1,'show wireless ap status',
                 check=[(ap1mac,'Managed','Success')],
                 waittime=5,retry=20,interval=5,IC=True)
# 因portfal认证服务器对超长url处理有问题，修改重定向各属性参数值长度
EnterConfigMode(switch1)
SetCmd(switch1,'radius source-ipv4 ' + StaticIpv4_ac1)
SetCmd(switch1,'radius-server key test')
SetCmd(switch1,'radius-server authentication host ' + Radius_server)
SetCmd(switch1,'radius-server accounting host ' + Radius_server)
SetCmd(switch1,'radius nas-ipv4 ' + StaticIpv4_ac1)
SetCmd(switch1,'aaa group server radius wlan')
SetCmd(switch1,'server ' + Radius_server)
EnterConfigMode(switch1)
SetCmd(switch1,'aaa enable')
SetCmd(switch1,'aaa-accounting enable')
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'enable')
SetCmd(switch1,'authentication-type external')
SetCmd(switch1,'external portal-server server-name eportal ipv4 '+ Radius_server)
SetCmd(switch1,'free-resource 1 destination ipv4 ' + Radius_server +'/32 source any')
SetCmd(switch1,'configuration 1 ')
SetCmd(switch1,'enable')
SetCmd(switch1,'radius accounting ')
SetCmd(switch1,'protocol http')
SetCmd(switch1,'radius-acct-server wlan')
SetCmd(switch1,'radius-auth-server wlan')
SetCmd(switch1,'redirect attribute url-after-login enable')
SetCmd(switch1,'redirect attribute ssid enable ')
SetCmd(switch1,'redirect attribute nas-ip enable')
SetCmd(switch1,'redirect attribute apmac enable')
SetCmd(switch1,'redirect attribute apmac name 1234567890123456789')
SetCmd(switch1,'redirect attribute custom-string name 123456789012345677890')
# 部分产品nas-ip name属性存在bug，目前配置成wlanacip以外的任何值都会导致失败!!!!!
# SetCmd(switch1,'redirect attribute nas-ip name wlanacip')
SetCmd(switch1,'redirect attribute nas-ip name 12345678')
SetCmd(switch1,'redirect attribute ssid name 1234567890123456789')
SetCmd(switch1,'redirect attribute usermac enable')
SetCmd(switch1,'redirect attribute usermac name 12345678901234567890')
SetCmd(switch1,'ac-name 0100.0010.0'+EnvNo+'0.01')
SetCmd(switch1,'redirect url-head http://192.168.10.101/a79.htm')
SetCmd(switch1,'portal-server ipv4 eportal')
SetCmd(switch1,'free-resource 1')
SetCmd(switch1,'interface ws-network 1')

WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# res1 = 0
#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#操作
#在STA1上连接test1
#
#预期
#连接成功
################################################################################

printStep(testname,'Step 2',
          'STA1connect to network 1,',
          'STA1dhcp and get 192.168.91.x ip')

sta1_ipv4 = ''

res1=res2=1

#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name4,bssid=ap1mac_lower)
IdleAfter(10)
#获取STA1的地址
#获取STA1的地址
sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
res2 = sta1_ipresult['res']  

#result
printCheckStep(testname, 'Step 2',res1,res2)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 3
    #操作
    #客户端STA1访问http://www.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.com
    #
    #预期
    #STA1被重定向到Portal认证页面
    ################################################################################

    printStep(testname,'Step 3',
              'STA1 http connect http://www.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.com,')

    web = web_init(sta1_host)
    if None != web:
        res1 = web_open(web,'http://1.1.1.1')
        if res1['status']:
            res2 = is_portal_page(web)
            if res2['status']:
                res3 = 0
            else:
                res3 = 1
                printRes('is_portal_page(web) status false')
        else:
            res3 = 1
            printRes('web_open(web,\'http://1.1.1.1\')')
    else:
        res3 =1
        printRes('web_init(sta1) status false')


    printCheckStep(testname, 'Step 3',res3)


    ################################################################################
    #Step 4
    #操作
    #输入用户名和密码
    #
    #预期
    #输入正确
    ################################################################################

    printStep(testname,'Step 4',
              'input username and password')


    #operate
    res1=res2=res3=1
    res1 = portal_login(web,'aaa','111')
    if res1['status']:
        res2 = 0
    else:
        printRes(res1)

    #result
    printCheckStep(testname, 'Step 4',res2)


    ################################################################################
    #Step 5
    #操作
    #客户端主动下线。
    #
    #预期
    #下线成功
    ################################################################################

    printStep(testname,'Step 5',
              'STA1 logout.')

    res1 = portal_logout(web)
    if res1 != None:
        if res1['status']:
            res2 = 0
        else:
            res2 =1
            printRes(res1)

    printCheckStep(testname, 'Step 5',res2)
    # 关闭firefox窗口
    res1 = web_close(web)
    printRes(res1)
    if not res1['status']:
        CMDKillFirefox(sta1)
################################################################################
#Step 6
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 6',
          'Recover initial config for switches.')

#operate

WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

EnterNetworkMode(switch1,'1')
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan '+Vlan4091)
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'disable')
SetCmd(switch1,'no configuration 1')
SetCmd(switch1,'no external portal-server ipv4 server-name eportal')
SetCmd(switch1,'no free-resource 1')
EnterConfigMode(switch1)
SetCmd(switch1,'no radius source-ipv4')
SetCmd(switch1,'no radius-server key')
SetCmd(switch1,'no aaa group server radius wlan')
SetCmd(switch1,'no radius nas-ipv4')
SetCmd(switch1,'no aaa enable')
SetCmd(switch1,'no aaa-accounting enable')
SetCmd(switch1,'no radius-server authentication host ' + Radius_server)
SetCmd(switch1,'no radius-server accounting host ' + Radius_server)

# SetCmd(ap1,'set management vlan-id',Vlan20)
# SetCmd(ap1,'set untagged-vlan vlan-id',Vlan20)
# ApSetcmd(ap1,Ap1cmdtype,'set_management_vlanid','1')
# ApSetcmd(ap1,Ap1cmdtype,'set_untagged_vlanid','1',commitflag=True)

EnterWirelessMode(switch1)
EnterApProMode(switch1,'1')
SetCmd(switch1,'no','management vlan')
SetCmd(switch1,'ethernet native-vlan 1')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# 配置下发后，ap的management vlan和ethernet native-vlan已经修改，
# 但是s3的端口配置没有修改，导致AP和AC之间不通，AP会下线
# （注意：此处必须先等AP下线后再修改S3配置）
CheckSutCmd(switch1,'show wireless ap status',
            check=[(ap1mac,'Failed','Not Config')],
            waitflag=False,retry=10,interval=5,IC=True)
# 修改S3端口配置  
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    EnterConfigMode(switch3)
    SetCmd(switch3,'no vlan 2')
    SetCmd(switch3,'Interface ',s3p3)
    SetCmd(switch3,'switchport mode access ')
    SetCmd(switch3,'switchport access vlan ',Vlan20)
else:
    EnterConfigMode(switch3)
    SetCmd(switch3,'no vlan 2')
    SetCmd(switch3,'Interface ',s3p3)
    SetCmd(switch3,'switchport mode trunk')
    SetCmd(switch3,'switchport trunk allowed vlan all')
    SetCmd(switch3,'switchport trunk native vlan',Vlan20)

IdleAfter(20)
res1=CheckSutCmd(switch1,'show wireless ap status',
                 check=[(ap1mac,'Managed','Success')],
                 waittime=5,retry=20,interval=5,IC=True)
# EnterWirelessMode(switch1)
# EnterApProMode(switch1,'1')
# SetCmd(switch1,'no','management vlan')
# SetCmd(switch1,'ethernet native-vlan 1')



# WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#end
printTimer(testname, 'End')


