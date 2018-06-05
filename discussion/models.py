from django.db import models
from django.contrib.auth.models import User
from dashboard.models import classrooms


class Discussion(models.Model):
	message=models.TextField(max_length=250)
	time=models.DateTimeField()
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	classroom=models.ForeignKey(classrooms,on_delete=models.CASCADE)

	def __str__(self):
		return 'User : '+self.user.username + ' - Time : '+ str(self.time) + ' Message : ' + self.message 


