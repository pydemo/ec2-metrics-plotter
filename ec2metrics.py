"""## Plots EC2 CPUUtilization metric for given instance id.
##
## Generates matplotlib plots for given instance/statistic/metric.
##
Usage:  
#---------------------------------------------------------------------- 
#FreeUkraine #SaveUkraine #StopRussia #PutinKhuilo #CrimeaIsUkraine
#----------------------------------------------------------------------
  set AWS_ACCESS_KEY_ID=<you access key>
  set AWS_SECRET_ACCESS_KEY=<you secret key>
  set AWS_DEFAULT_REGION=<your region > (for example:us-west-2 ) 
  ec2metrics.exe [<instance>] [<period_min>] [<from_min>] [<to_min>] 
	[<statistic>] [<metric_name>] [<namespace>]
	[<show_plot> or <show_report>] 
	[<plot_dir>] [<plot_dir>] 
	
	[-b] --instance 	-- EC2 instance name (i-********).
	[-p] --period_min 	-- Aggregation interval (5 min).
	[-f] --from_min  	-- Start from, min (60).
	[-t] --to_min 	 	-- End at, min (0 - present).
	[-s] --statistic  	-- Statistic type (Average).
	   Could be one of: Sum,Maximum,Minimum,SampleCount,Average
	[-m] --metric_name  -- Metric name (CPUUtilization)
	   Could be one of:
		CPUUtilization,NetworkIn,NetworkOut,NetworkPacketsIn,
		NetworkPacketsOut,DiskWriteBytes,DiskReadBytes,DiskWriteOps,
		DiskReadOps,CPUCreditBalance,CPUCreditUsage,StatusCheckFailed,
		StatusCheckFailed_Instance,StatusCheckFailed_System
	[-g] --namespace  	-- CloudWatch namespace, 
	container for metric (AWS/EC2).
	
	[-r] --show_plot  	-- Open plotter window (False).
	[-n] --show_report  -- Open browser with html report (True).
	
	[-d] --plot_dir  	-- Target plot dir (plots).
	[-e] --plot_dir  	-- Timestamp for to append to plot_dir 
	(current date).
	
	Index.html is generated in <plot_dir>\<timestamp>
	
	Author: Alex Buzunov(alex_buz@yahoo.com)
	
"""

import boto3
from datetime import datetime, timedelta
from pprint import pprint
import html.parser
import sys
import tkinter
import tkinter.filedialog
import os
import matplotlib.pyplot as plt
from matplotlib import rcParams
#import static
import webbrowser
import types
import imp

from optparse import OptionParser
region=None
e=sys.exit
def import_module(filepath):
	class_inst = None
	#expected_class = 'MyClass'

	mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])
	assert os.path.isfile(filepath), 'File %s does not exists.' % filepath
	if file_ext.lower() == '.py':
		py_mod = imp.load_source(mod_name, filepath)

	elif file_ext.lower() == '.pyc':
		py_mod = imp.load_compiled(mod_name, filepath)
	return py_mod


abspath=os.path.abspath(os.path.dirname(sys.argv[0]))
	
static = import_module(os.path.join(abspath,'config','static.py'))


def get_instance_stats(c,instance, metric_name,statistic,namespace):
	global opt
	#print (statistic)
	s=c.get_metric_statistics(
		Period=opt.period_min*60,
		StartTime=datetime.utcnow() - timedelta(seconds=opt.from_min*60),
		EndTime=datetime.utcnow() - timedelta(seconds=opt.to_min*60),
		MetricName=metric_name,
		Namespace=namespace, #Unit='Percent',
		Statistics=[statistic],
		Dimensions=[{'Name':'InstanceId','Value':instance}]
	)
	return s
def plot_instance_metric(opt, instance, metric_name,statistic):
	global tss, region
	delta=opt.from_min-opt.to_min
	assert delta>0, 'from_min (%d) has to be farther in the past than to_min (%d)' % (opt.from_min,opt.to_min)
	s=get_instance_stats(c,instance=instance,metric_name=metric_name,statistic=statistic, namespace=opt.namespace)
	#pprint(s)
	
	#print (opt.metric_name, s['ResponseMetadata']['HTTPStatusCode'],len(s['Datapoints']))
	#e(0)
	#pprint(s)
	a={}
	week=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
	for i in s['Datapoints']: 
		a[i['Timestamp']]=i[statistic]
	if 0:
		for ts in sorted(a.keys()):
			#pprint(dir(ts))
			#print(ts.utctimetuple)
			e(0)
			print ('%s %02d, %02d:%02d -> %s:%s' % (week[ts.weekday()], ts.day , ts.hour,ts.minute,statistic, a[ts]))		
	assert len(s['Datapoints'])>0, 'No datapoints exist for metric "%s".' % metric_name
	assert a, 'No metrics exist for this interval.'
	assert len(s['Datapoints'])>1, 'Not enought datapoints to plot (%d).' % len(s['Datapoints'])
	assert not opt.period_min>opt.from_min-opt.to_min, 'Period is larger than delta.'
	assert s['ResponseMetadata']['HTTPStatusCode'] in [200], 'Error: HTTPStatusCode %s' % s['ResponseMetadata']['HTTPStatusCode']
	prev=0
	nonzero= len([i for i in filter(None, a.values())])
	
	print ('%03s(%04d/%04d): %s: %s: %s' % (s['ResponseMetadata']['HTTPStatusCode'],nonzero,len(s['Datapoints']),instance,metric_name,statistic))		
		
	vals= [a[i] for i in sorted(a.keys())]
	keys=list(a.keys())
	keys.sort()
	
	
	show_keys= {float(i):'%s\n%s %02d' % (keys[i].strftime('%I:%M %p' ),week[keys[i].weekday()], keys[i].day) for i in range(len(keys))}
	font = {'family' : 'normal',        'weight' : 'normal',        'size'   : 10}
	rcParams.update({'font.size': 10})	
	fig, ax = plt.subplots()
	
	s = vals 
	ns=opt.namespace.replace('/','-')
	plt.plot([i for i in range(len(keys))],vals)
	fig.canvas.draw()
	
	plt.ylabel('%s (%s, %s, %smin )' % (region, opt.namespace, statistic, opt.period_min))
	fts=datetime.utcnow() - timedelta(seconds=opt.from_min*60)
	tts=datetime.utcnow() - timedelta(seconds=opt.to_min*60)
	plt.title('%s for %s, %dhrs %dmin\n(%smin from %s to %s)' % (metric_name, instance,round((opt.from_min-opt.to_min)/60),(opt.from_min-opt.to_min)%60,opt.from_min-opt.to_min, fts.strftime('%Y/%m/%d %I:%M %p'),tts.strftime('%Y/%m/%d %I:%M %p')))
	plt.grid(True)
	
	labels =[str(i) for i in range(len(keys))]
	lbls=ax.get_xticklabels()

	for i in range(len(ax.get_xticklabels())):
		item=ax.get_xticklabels()[i]
		txt= item.get_text().encode("ascii",'ignore').decode("windows-1252")
		if float(txt) in list(show_keys.keys()):
			new_txt='%s\n%s' % 	(txt,show_keys[int(float(txt))] )
			lbls[i].set_text(new_txt)
		else:
			pass
	ax.set_xticklabels(lbls)
	fig.canvas.set_window_title('Instance:%s, Period:%d sec.' % (instance,opt.period_min*60))
	to_dir=os.path.join(opt.plot_dir,tss,'by_metric',metric_name,statistic,str(opt.period_min))
	by_instance=os.path.join(opt.plot_dir,tss,'by_instance',instance,str(opt.period_min))
	if not os.path.isdir(to_dir):
		os.makedirs(to_dir)
	if not os.path.isdir(by_instance):
		os.makedirs(by_instance)			
	plt.savefig(os.path.join(to_dir,"%s.%s.%s.%s.png" % (metric_name,statistic,opt.period_min,instance)))
	plt.savefig(os.path.join(by_instance,"%s.%s.%s.%s.png" % (metric_name,statistic,opt.period_min,instance)))
	if opt.show_plot:
		plt.show()
	plt.close(fig)
				
	
if __name__ == "__main__":	
	
	parser = OptionParser()
	
	parser.add_option("-b", "--instance", dest="instance", default='')
	parser.add_option("-p", "--period_min", dest="period_min", type=int,default=5)
	parser.add_option("-f", "--from_min", dest="from_min", type=int, default=60)
	parser.add_option("-t", "--to_min", dest="to_min",type=int, default=0)
	parser.add_option("-s", "--statistic", dest="statistic",type=str, default='Average') #Maximum
	parser.add_option("-m", "--metric_name", dest="metric_name",type=str, default='CPUUtilization')
	parser.add_option("-g", "--show_plot", action="store_true",dest="show_plot", default=False)
	parser.add_option("-r", "--show_report", action="store_true",dest="show_report", default=False)
	parser.add_option("-n", "--namespace", dest="namespace",type=str, default='AWS/EC2')
	parser.add_option("-d", "--plot_dir", dest="plot_dir",type=str, default='plots')
	parser.add_option("-e", "--timestamp", dest="timestamp",type=str, default=datetime.now().strftime('%Y%m%d_%H%M%S'))
	
	
	
	(opt, _) = parser.parse_args()
	
	if not os.path.isabs(opt.plot_dir):
		opt.plot_dir=os.path.abspath(opt.plot_dir)
	#e(0)
	tss=opt.timestamp
	
	if len(sys.argv)<2:
		print (__doc__)
		e(1)
	if not opt.instance:
		print('EC2 fleet metrics are not supported. Exiting....')
		e(1)
	assert os.getenv('AWS_ACCESS_KEY_ID'), 'AWS_ACCESS_KEY_ID env variable is not set.'
	assert os.getenv('AWS_SECRET_ACCESS_KEY'), 'AWS_SECRET_ACCESS_KEY env variable is not set.'
	region=os.getenv('AWS_DEFAULT_REGION')
	assert region, 'AWS_DEFAULT_REGION env variable is not set.'	
	c = boto3.client('cloudwatch')
	for instance in opt.instance.split(','):
		instance=instance.strip('"').strip("'")
		for metric_name in opt.metric_name.split(','): #['CPUUtilization','NetworkIn','NetworkOut','NetworkPacketsIn','NetworkPacketsOut','DiskWriteBytes','DiskReadBytes','DiskWriteOps','DiskReadOps','CPUCreditBalance','CPUCreditUsage','StatusCheckFailed','StatusCheckFailed_Instance','StatusCheckFailed_System']:
			#opt.metric_name=m
			for statistic in opt.statistic.split(','): #[ 'Sum', 'Maximum', 'Minimum', 'SampleCount', 'Average' ]:
				#opt.statistic=s
				if 1:
					plot_instance_metric(opt, instance, metric_name,statistic)
	#tss='20160327_093502'
	plot_dir=os.path.join(opt.plot_dir,tss,'by_metric')
	#by_instance=os.path.join('plots',tss,'by_instance',instance,str(opt.period_min))				
	files=[]
	for root, directories, filenames in os.walk(plot_dir):
		for filename in filenames: 
			files.append(os.path.join(root,filename))
	#print(files)
	
	#out_html='plot_index.html'
	hfile = os.path.join(opt.plot_dir,tss,static.index)
	#e(0)
	div_size = (static.thum_size+55)*static.plots_per_row+20
	if len(files)<static.plots_per_row:
		div_size =(static.thum_size+55)*len(files)+20
	#print(len(files),div_size)
	if div_size<900:
		div_size=900
	
	filename, file_extension = os.path.splitext(__file__)
	cmd='%s.%s' % (filename,'exe')
	for attr in sorted(opt.__dict__):
		if opt.__dict__[attr]:
			if type(opt.__dict__[attr]) == type(True): 
				cmd +=' --%s' % (attr)
			else:
				cmd +=' --%s %s' % (attr, opt.__dict__[attr])
	#print (cmd)
	cmd_len=(div_size)/2
	if 1:
		prefix=os.path.dirname(hfile) 
		#e(0)
		with open(hfile, 'w') as index_file:
			
			index_file.write(static.header % ('EC2 Metrics generator.',div_size))
			index_file.write(static.timestamp % (region))
			index_file.write('<table><th align=Left> Argsuments<th align=Left>CLI Command')
			index_file.write('<tr><td>')
			index_file.write('<table>')
			for attr in sorted(opt.__dict__):
				index_file.write('<tr>')
				if type(opt.__dict__[attr]) in [str]:
					index_file.write('<td><b>%s<td style="max-width:%dpx;"><span style="max-width:%dpx;">%s</span>' % (attr,cmd_len-100,cmd_len-100,opt.__dict__[attr]))	
				else:
					index_file.write('<td><b>%s<td>%s' % (attr,opt.__dict__[attr]))	
				
			
			index_file.write('</table><td valign=top style="max-width:%dpx;" >' % cmd_len)
			index_file.write('<span style="max-width:%dpx;">%s</span>' % (cmd_len,cmd))
			
			

			index_file.write('</table>\n<br>')
			page_count = 0
			index_file.write('<table>')
			for i in range(0,len(files),static.plots_per_row):
				#print(i)
				index_file.write('<tr>')
				for j in range(static.plots_per_row):
					#print(j, i+j)
					#index_file.write(static.img_src % ('150',img))
					index_file.write('<td>')
					if i+j<len(files):
						img=files[i+j]
						bn=os.path.basename(img)
						index_file.write(' '.join(bn.split('.')[:-1]))
				index_file.write('<tr >')
				for j in range(static.plots_per_row):
					#print(j, i+j)
					#index_file.write(static.img_src % ('150',img))
					index_file.write('<td>')
					if i+j<len(files):
						img=files[i+j]
						bn=os.path.basename(img)
						#print(img)
						relpath=os.path.relpath(os.path.dirname(img), prefix) 
						#e(0)
						rel_img=os.path.join(relpath,bn)
						index_file.write(static.url_img % (rel_img,static.thum_size,bn,rel_img))

			index_file.write('</table>')	
			index_file.write(static.footer)
	print ('\nReport is at: %s' % hfile)
	if opt.show_report:
		webbrowser.open_new(hfile)
		
