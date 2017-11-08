from django.shortcuts import render
from ws4redis.redis_store import RedisMessage
from ws4redis.publisher import RedisPublisher
from django.shortcuts import HttpResponse
from rewardingroads.forms import *
from rewardingroads.decorators import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings

@user_session_set
def index(request):
	user = Traveller.objects.get(name=request.session['username'])
	total_reports = Report.objects.filter(reporter=user).exclude(trigger=3)
	verified_reports = Report.objects.filter(reporter=user).filter(processed=1)
	context = {
		'user' : user,
		'total_reports' : total_reports,
		'verified_reports' : verified_reports
	}
	return render(request,'rewardingroads/home.html',context)

def govt(request):
	operators = Operator.objects.order_by('penalty')
	pendingReports = Report.objects.filter(processed=0).count()
	pendingInformation = Information.objects.filter(status=0).count()
	totalPenalty = 0
	for operator in operators:
		totalPenalty += operator.penalty
	travellerCount = Traveller.objects.all().count()
	context = {
		'operators' : operators,
		'pendingReports' : pendingReports,
		'pendingInformation' : pendingInformation,
		'travellerCount' : travellerCount,
		'totalPenalty' : totalPenalty
	}
	return render(request,'rewardingroads/govt.html',context)

@user_session_set
def drive(request):
	user = Traveller.objects.get(name=request.session['username'])
	roads = Road.objects.all()
	unchecked = Information.objects.filter(status=0).filter(trust__lte=0.90)
	complete = []
	for ind,info in enumerate(unchecked):
		temp = [float(info.latitude),float(info.longitude),ind+1]
		complete.append(temp)
	final = json.dumps(complete)
	context = {
		'user' : user,
		'roads' : roads,
		'toBeChecked' : final,
		'unchecked' : unchecked,
		'YOUR_API_KEY' : settings.YOUR_API_KEY
	}
	return render(request,'rewardingroads/drive.html',context)

def login(request):
	request.session.pop('username',None)
	if request.method == "POST":
		print(request.POST)
		username = request.POST.get('name','nikhil96sher')
		request.session['username'] = username
		return HttpResponseRedirect('/roads/')
	return render(request,'rewardingroads/login.html')

revmap = {
	'Decelaration' : 1,
	'Lane Switching' : 2,
	'Confirmation' : 3
}

@csrf_exempt
def report(request):
	try:
		data = json.loads(request.body)
		rows = data['myrows']
		road = Road.objects.get(pk = int(data['road']))
		user = Traveller.objects.get(name = request.session['username'])
		for report in rows:
			# print(report)
			# Getting Request Parameters
			latitude = float(report['Latitude'])
			longitude = float(report['Longitude'])
			trigger = revmap[report['Trigger Type']]
			severity = int(report['Severity'])
			time = report['Incident Time']

			#Create Report Instance
			d = Report()
			d.reporting_time = time
			d.reporter = user
			d.latitude = latitude
			d.longitude = longitude
			d.road = road
			d.trigger = trigger
			d.severity = severity

			# Create User Instance
			user.last_latitude = latitude
			user.last_longitude = longitude
			user.save()

			# Computing Information Instance
			delta = 0.01
			lat = round(latitude,4)
			lon = round(longitude,4)
			infos = Information.objects.filter(latitude__lte=lat+delta, latitude__gte=lat-delta).filter(longitude__lte=lon+delta, longitude__gte=lon-delta)

			if(infos.count() != 0):
				info = infos[0]
				if trigger == 3 and severity <= 2:
					print("YO CASE")
					info.status = 1
					info.save()
				info.last_report_time = d.reporting_time
				info.first_report_time = info.last_report_time
				info.trust = ((info.report_count * info.trust) + (user.trust))/(info.report_count+1)
				info.avg_severity = (info.avg_severity*info.report_count)/(info.report_count+1)
				info.report_count += 1
				info.save()
			else:
				info = Information()
				info.latitude = lat
				info.longitude = lon
				info.trust = user.trust
				info.road = road
				info.last_report_time = d.reporting_time
				info.first_report_time = info.last_report_time
				info.avg_severity = severity
				info.save()
			d.information = info
			d.save()
		return HttpResponse("success")
	except Exception as e:
		print(e)
		return HttpResponse("error")