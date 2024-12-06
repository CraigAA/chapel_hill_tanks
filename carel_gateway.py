from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils


tanks={	'1':{'ip':"10.53.194.157", 'unit_id':195},
		'2':{'ip':"10.53.194.157", 'unit_id':194},
		'3':{'ip':"10.53.194.157", 'unit_id':193},
		'9':{'ip':"10.53.194.158", 'unit_id':195},
		'10':{'ip':"10.53.194.158", 'unit_id':194},
		'11':{'ip':"10.53.194.159", 'unit_id':195},
		'12':{'ip':"10.53.194.159", 'unit_id':194},
		'13':{'ip':"10.53.194.160", 'unit_id':195},
		'14':{'ip':"10.53.194.160", 'unit_id':194},
		'15':{'ip':"10.53.194.161", 'unit_id':195},
		'16':{'ip':"10.53.194.161", 'unit_id':194},
		'17':{'ip':"10.53.194.162", 'unit_id':195},
		'18':{'ip':"10.53.194.162", 'unit_id':194},
		'19':{'ip':"10.53.194.163", 'unit_id':195},
		'20':{'ip':"10.53.194.163", 'unit_id':194},
		'22':{'ip':"10.53.194.164", 'unit_id':195},
		'23':{'ip':"10.53.194.164", 'unit_id':194},
		'24':{'ip':"10.53.194.164", 'unit_id':193},
		'31':{'ip':"10.53.194.165", 'unit_id':195},
		'32':{'ip':"10.53.194.165", 'unit_id':194},
		'35':{'ip':"10.53.194.166", 'unit_id':195},
		'36':{'ip':"10.53.194.166", 'unit_id':194},
		'37':{'ip':"10.53.194.166", 'unit_id':193},
		'R21':{'ip':"10.53.194.167", 'unit_id':195},
		'R22':{'ip':"10.53.194.167", 'unit_id':194},
		'R23':{'ip':"10.53.194.167", 'unit_id':193},
		'R24':{'ip':"10.53.194.167", 'unit_id':192},
		'R25':{'ip':"10.53.194.167", 'unit_id':191},
		'200':{'ip':"10.53.194.168", 'unit_id':195},
		'201':{'ip':"10.53.194.169", 'unit_id':194},
		'202':{'ip':"10.53.194.169", 'unit_id':195},
		'203':{'ip':"10.53.194.170", 'unit_id':194},
		'204':{'ip':"10.53.194.170", 'unit_id':195},
		'210':{'ip':"10.53.194.171", 'unit_id':194},
		'211':{'ip':"10.53.194.171", 'unit_id':195},
		'212':{'ip':"10.53.194.172", 'unit_id':194},
		'213':{'ip':"10.53.194.172", 'unit_id':195},
		'214':{'ip':"10.53.194.173", 'unit_id':194},
		'215':{'ip':"10.53.194.173", 'unit_id':195}}

for t in tanks:
	try:
		client = ModbusClient(tanks[t]['ip'], port=8899, unit_id=tanks[t]['unit_id'], auto_open=True, auto_close=True,timeout=5)
		success = client.open()
	
		path='[edge]Tank Farm/Tank_'
		
		stpt_value=system.tag.readBlocking([path + t + '/STPT_TMP'])[0].value*10.0
		
#		client.write_single_register(15,stpt_value)
		
		read_temp = client.read_holding_registers(2, 1)[0]/10.0
		
		read_stpt = client.read_holding_registers(15,1)[0]/10.0
		
		system.tag.writeBlocking([path + t + '/STPT_TMP', path + t + '/STS_TMP', path + t + '/HB_LAST_UPDATE'], 
			[read_stpt, read_temp, system.date.now()])
		
		
		read_lo = bool(client.read_coils(15,1)[0])
		read_hi = bool(client.read_coils(16,1)[0])
		
		system.tag.writeBlocking(['[edge]Tank Farm/Tank_test/SETPOINT_ALARM_LO','[edge]Tank Farm/Tank_test/SETPOINT_ALARM_HI'], [read_lo,read_hi])
	except:
		logger=system.util.getLogger('Carel-connection')
		logger.info('Failed to Connect to Carel for Tank ' + t)