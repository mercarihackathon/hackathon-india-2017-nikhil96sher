from django.forms import ModelForm
from rewardingroads.models import *

class ReportForm(ModelForm):
	class Meta:
		model = Report
		fields = ['incident','road']