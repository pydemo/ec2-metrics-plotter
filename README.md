# CloudWatch AWS/EC2 instance metrics plotter.
Purpose:
 - Generate and plot statistics for CloudWatch EC2 instance.
 - All Metrics and statistics are supported
 
Included:

+ *Statistics*:
	Sum,Maximum,Minimum,SampleCount,Average
	
+ *Metrics*:
	CPUUtilization,NetworkIn,NetworkOut,NetworkPacketsIn,
	NetworkPacketsOut,DiskWriteBytes,DiskReadBytes,DiskWriteOps,
	DiskReadOps,CPUCreditBalance,CPUCreditUsage,StatusCheckFailed,
	StatusCheckFailed_Instance,StatusCheckFailed_System
	
Wrote using Python/boto3.
Compiled using PyInstaller

##Version

OS|Platform|Version 
---|---|---- | -------------
Windows|32bit|[0.1.0 beta]

##Purpose

- Generate plots for AWS-ECS metrics and statistics.
- Helps you generate plots on demand and review them using generated html report.

## How it works
- plotEC2metrics.exe connects to EC2 and reads datapoints for given CloudWatch EC2 instance/metric/statistic combo.
- Using matplotlib plot is created and saved on the filesystem.
- Html report is generated allowing preview saved metric plots.
- It will not work for group CloudWatch EC2 instances metrics.

##Audience

Database/ETL developers, Data Integrators, Data Engineers, Business Analysts, AWS Developers, DevOps

##Designated Environment
Pre-Prod (UAT/QA/DEV)

##Usage

```
C:\Python35-32>dist\ec2metrics\ec2metrics.exe
## Plots EC2 CPUUtilization metric for given instance id.
##
## Generates matplotlib plots for given instance/statistic/metric.
##
Usage:
  set AWS_ACCESS_KEY_ID=<you access key>
  set AWS_SECRET_ACCESS_KEY=<you secret key>
  set AWS_DEFAULT_REGION=<your region > (for example:us-west-2 )
  ec2metrics.exe [<instance>] [<period_min>] [<from_min>] [<to_min>]
        [<statistic>] [<metric_name>] [<namespace>]
        [<show_plot> or <show_report>]
        [<plot_dir>] [<plot_dir>]

        [-b] --instance         -- EC2 instance name (i-********).
        [-p] --period_min       -- Aggregation interval (5 min).
        [-f] --from_min         -- Start from, min (60).
        [-t] --to_min           -- End at, min (0 - present).
        [-s] --statistic        -- Statistic type (Average).
           Could be one of: Sum,Maximum,Minimum,SampleCount,Average
        [-m] --metric_name  -- Metric name (CPUUtilization)
           Could be one of:
                CPUUtilization,NetworkIn,NetworkOut,NetworkPacketsIn,
                NetworkPacketsOut,DiskWriteBytes,DiskReadBytes,DiskWriteOps,
                DiskReadOps,CPUCreditBalance,CPUCreditUsage,StatusCheckFailed,
                StatusCheckFailed_Instance,StatusCheckFailed_System
        [-g] --namespace        -- CloudWatch namespace,
        container for metric (AWS/EC2).

        [-r] --show_plot        -- Open plotter window (False).
        [-n] --show_report  -- Open browser with html report (True).

        [-d] --plot_dir         -- Target plot dir (plots).
        [-e] --plot_dir         -- Timestamp for to append to plot_dir
        (current date).

        Index.html is generated in <plot_dir>\<timestamp>

```

##Environment variables

```
  set AWS_ACCESS_KEY_ID=<you access key>
  set AWS_SECRET_ACCESS_KEY=<you secret key>
  set AWS_DEFAULT_REGION=<your region > (for example:us-west-2 )
```

#Examples

### Plot "Average,Minimum" for "NetworkIn" CloudWatch EC2 metric.


```
ec2metrics.exe --instance i-fe9cea26 -f 1000  -p 10  -s Average,Minimum -m NetworkIn  -r

200(0100/0100): i-fe9cea26: NetworkIn: Sum
200(0100/0100): i-fe9cea26: NetworkIn: Maximum
200(0100/0100): i-fe9cea26: NetworkIn: Minimum
200(0100/0100): i-fe9cea26: NetworkIn: SampleCount
200(0100/0100): i-fe9cea26: NetworkIn: Average

Report is at: C:\Python35-32\plots\20160327_220118\index.html

```

####Result:

![NetworkIn/Average/10min] (https://raw.githubusercontent.com/alexbuz/EC2_Metrics_Plotter/master/plots/EC2_NetworkIn/by_metric/NetworkIn/Average/10/NetworkIn.Average.10.i-fe9cea26.png)

#### Html report
Report is generated with preview for all plots created with this job.
![ALL](https://raw.githubusercontent.com/alexbuz/EC2_Metrics_Plotter/master/plot_reports/networkin.png)



### Plot "Sum,Maximum,Minimum,SampleCount,Average" stats for "CPUUtilization" CloudWatch EC2 metric.


```
ec2metrics.exe --instance i-fe9cea26 -f 500  -p 1  -s Sum,Maximum,Minimum,SampleCount,Average -m CPUUtilization  -r
200(0084/0099): i-fe9cea26: CPUUtilization: Sum
200(0084/0099): i-fe9cea26: CPUUtilization: Maximum
200(0000/0099): i-fe9cea26: CPUUtilization: Minimum
200(0099/0099): i-fe9cea26: CPUUtilization: SampleCount
200(0084/0099): i-fe9cea26: CPUUtilization: Average

Report is at: c:\Python35-32\plots\20160328_113906\index.html

```

####Result:

![CPUCreditUsage/Average/30min] (https://raw.githubusercontent.com/alexbuz/EC2_Metrics_Plotter/master/plots/CPUUtilization/by_instance/i-fe9cea26/1/CPUUtilization.Average.1.i-fe9cea26.png)


### Plot "Sum,Maximum,Minimum,SampleCount,Average" stats for "CPUCreditUsage" CloudWatch EC2 metric.


```
ec2metrics.exe --instance i-fe9cea26 -f 6000  -p 30  -s Sum,Maximum,Minimum,SampleCount,Average -m CPUCreditUsage  -r -t 3000 -e CPUCreditUsage
200(0006/0027): i-fe9cea26: CPUCreditUsage: Sum
200(0006/0027): i-fe9cea26: CPUCreditUsage: Maximum
200(0001/0027): i-fe9cea26: CPUCreditUsage: Minimum
200(0027/0027): i-fe9cea26: CPUCreditUsage: SampleCount
200(0006/0027): i-fe9cea26: CPUCreditUsage: Average
Report is at: c:\Python35-32\plots\CPUCreditUsage\index.html

```

####Result:

![CPUCreditUsage/Average/30min] (https://raw.githubusercontent.com/alexbuz/EC2_Metrics_Plotter/master/plots/CPUCreditUsage/by_metric/CPUCreditUsage/Average/30/CPUCreditUsage.Average.30.i-fe9cea26.png)


### Plot all stats for all CloudWatch EC2 metrics.


```
c:\Python35-32>dist\ec2metrics\ec2metrics.exe --from_min 3000 --instance 'i-fe9cea26,i-fe9cea26' --metric_name CPUUtilization,NetworkIn,NetworkOut,NetworkPacketsIn,NetworkPacketsOut,DiskWriteBytes,DiskReadBytes,DiskWriteOps,DiskReadOps,CPUCreditBalance,CPUCreditUsage,StatusCheckFailed,StatusCheckFailed_Instance,StatusCheckFailed_System --namespace AWS/EC2 --period_min 1 --plot_dir C:\Python35-32\plots --statistic Average,Minimum,Maximum,Sum  --to_min 2000 -r -e All_Metrics

200(0174/0200): i-fe9cea26: CPUUtilization: Average
200(0001/0200): i-fe9cea26: CPUUtilization: Minimum
200(0174/0200): i-fe9cea26: CPUUtilization: Maximum
200(0174/0200): i-fe9cea26: CPUUtilization: Sum
200(0200/0200): i-fe9cea26: NetworkIn: Average
...
200(0000/1000): i-fe9cea26: StatusCheckFailed_Instance: Sum
200(0000/1000): i-fe9cea26: StatusCheckFailed_System: Average
200(0000/1000): i-fe9cea26: StatusCheckFailed_System: Minimum
200(0000/1000): i-fe9cea26: StatusCheckFailed_System: Maximum
200(0000/1000): i-fe9cea26: StatusCheckFailed_System: Sum

Report is at: C:\Python35-32\plots\All_Metrics\index.html

```

####Result:
One of the plots:
![NetworkIn/Average/10min] (https://raw.githubusercontent.com/alexbuz/EC2_Metrics_Plotter/master/plots/CPUCreditBalance/by_instance/i-fe9cea26/30/CPUCreditBalance.Sum.30.i-fe9cea26.png)

#### Html report
Report is generated with preview for all plots created with this job.
![ALL](https://raw.githubusercontent.com/alexbuz/EC2_Metrics_Plotter/master/plot_reports/all.png)


##Download
* [Master Release](https://github.com/alexbuz/EC2_Metrics_Plotter/archive/master.zip) -- `ec2metrics 0.1.0`
