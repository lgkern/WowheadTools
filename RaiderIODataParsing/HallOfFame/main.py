import json
import codecs 
import pandas

with codecs.open('argus-mythic-kills.json', 'r', 'utf-8') as file:
	d = json.load(file)	
	hordeKills = []
	allianceKills = []
	allKills = d['bossRankings']
	realms = []
	for kill in allKills:
		if kill['guild']['realm']['id'] in realms:
			kill['realmFirst'] = False
		else:
			realms.append(kill['guild']['realm']['id'])
			kill['realmFirst'] = True
		#print(kill['realmFirst'])
		if kill['guild']['faction'] == 'horde':
			hordeKills.append(kill)
		else:
			allianceKills.append(kill)

	#print(realms)

	print('Total Guilds: {2}\tHorde Guilds: {0}\tAlliance Guilds: {1}\n'.format(len(hordeKills), len(allianceKills), len(allKills)))
	print('Last Hall of Fame Rank Horde: {0}\tAlliance: {1}'.format(hordeKills[99]['rank'], allianceKills[99]['rank']))
	print('Last Hall of Fame Date Horde: {0}\tAlliance: {1}'.format(hordeKills[99]['encountersDefeated'][0]['firstDefeated'][:10], allianceKills[99]['encountersDefeated'][0]['firstDefeated'][:10]))

	hofNoRealmFirstH = 0
	hofNoRealmFirstA = 0
	hofAfter200H = 0
	hofAfter200A = 0
	realmFirstNoHoFH = 0
	realmFirstNoHoFA = 0
	noHofBefore200H = 0
	noHofBefore200A = 0

	for kill in hordeKills[:100]:
		if not kill['realmFirst']:
			hofNoRealmFirstH += 1	
		if kill['rank'] > 200:
			hofAfter200H += 1

	for kill in allianceKills[:100]:				
		if not kill['realmFirst']:
			hofNoRealmFirstA += 1
		if kill['rank'] > 200:
			hofAfter200A += 1

	for kill in hordeKills[100:]:
		if kill['realmFirst']:
			realmFirstNoHoFH += 1	
		if kill['rank'] <= 200:
			noHofBefore200H += 1

	for kill in allianceKills[100:]:				
		if kill['realmFirst']:
			realmFirstNoHoFA += 1
		if kill['rank'] <= 200:
			noHofBefore200A += 1


	print('Guilds that would receive HoF, but didnt get Realm First = {0}\tHorde: {1}\tAlliance: {2}'.format(hofNoRealmFirstH + hofNoRealmFirstA, hofNoRealmFirstH, hofNoRealmFirstA))				
	print('Guilds that got Realm First, but would not receive Hall of Fame = {0}\tHorde: {1}\tAlliance: {2}'.format(realmFirstNoHoFH + realmFirstNoHoFA, realmFirstNoHoFH, realmFirstNoHoFA))				
	print('Guilds that would receive HoF beyond top 200 overall = {0}\tHorde: {1}\tAlliance: {2}'.format(hofAfter200H + hofAfter200A, hofAfter200H, hofAfter200A))				
	print('Guilds that would not receive HoF but are top 200 overall = {0}\tHorde: {1}\tAlliance: {2}'.format(noHofBefore200H + noHofBefore200A, noHofBefore200H, noHofBefore200A))				

	print('Last Hall of Fame ')








	#df = pandas.DataFrame(data=d['bossRankings'])
	#print(df.axes)
	#print(len(df.filter(like='Horde', axis=1)))
	#print(len(data['bossRankings']))
	
