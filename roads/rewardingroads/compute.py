from rewardingroads.models import *

informations = Information.objects.filter(status=0)

reports = Report.objects.filter(processed=0)
infoAvailable = {}

for report in reports:
	try:
		infoAvailable[report.information].append(report)
	except:
		infoAvailable[report.information] = [report]

def getPenalty(information):
	report_counts = information.report_count
	cases = Information.objects.filter(status=0).filter(road__operator=information.road.operator).count()
	timeDelta = abs(information.last_report_time - information.first_report_time).seconds/3600.0
	return cases*10 + report_counts*100 + timeDelta*1000

## ALSO IF TIME DIFFERENCE B/W LAST ACTION AND CURRENT TIME IS GREATER THAN BIG DELTA

for information in infoAvailable:
	print("COMPUTING : ",repr(information))
	penalty = getPenalty(information)
	pSum = 0.0
	for report in infoAvailable[information]:
		pSum += float(report.severity)*(float(report.reporter.trust))
	worth = penalty/pSum
	operate = information.road.operator
	operate.penalty += penalty
	operate.save()
	delta1 = 0
	delta = 1
	for report in infoAvailable[information]:
		if abs(report.severity - information.avg_severity) < delta:
			delta1 += 1

	#get Information Trust - Deviation of Individual Reports from Severity
	print("EXISTING TRUST : ",information.trust)
	information.trust = information.trust + (1-information.trust)*(delta1/len(infoAvailable[information]))
	print("NEW TRUST : ",information.trust)
	information.save()

	for report in infoAvailable[information]:
		delta = worth*float(report.severity)*float(report.reporter.trust)
		report.credits = delta
		report.processed = 1
		traveller = report.reporter
		traveller.credits += delta
		#get User Trust = Deviation of Users' Reported Trust from Severity
		traveller.save()
		report.save()