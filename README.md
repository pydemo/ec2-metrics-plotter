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



## Other scripts
  - [DataWorm for Oracle](https://github.com/pydemo/DataWorm/blob/master/README.md) ad-hoc backup.
  - [TableHunter for Oracle](https://github.com/pydemo/TableHunter-For-Oracle) Win OS spooler
  
  - [Oracle -> Redshift](https://github.com/pydemo/Oracle-To-Redshift-Data-Loader/blob/master/README.md) data loader
  - [PostgreSQL -> Redshift](https://github.com/pydemo/PostgreSQL_To_Redshift_Loader/blob/master/README.md) data loader
  - [MySQL -> Redshift](https://github.com/pydemo/MySQL_To_Redshift_Loader/blob/master/README.md) data loader
  - [Oracle -> S3](https://github.com/pydemo/Oracle_To_S3_Data_Uploader/blob/master/README.md) data loader
  - [CSV -> Redshift](https://github.com/pydemo/CSV_Loader_For_Redshift/blob/master/README.md) data loader
  - [EC2 Metcics Plotter](https://github.com/pydemo/EC2_Metrics_Plotter/blob/master/README.md)
  - [Oracle->Oracle](https://github.com/pydemo/TabZilla/blob/master/README.md) data loader.
  - [Oracle->MySQL](https://github.com/pydemo/Oracle-to-MySQL-DataMigrator/blob/master/README.txt) data loader.
  - [CSV->S3](https://github.com/pydemo/S3_File_Uploader/blob/master/README.md) data uploader.
 
## Purpose

- Generate plots for AWS-ECS metrics and statistics.
- Helps you generate plots on demand and review them using generated html report.

## How it works
- ec2metrics.exe connects to EC2 and reads datapoints for given CloudWatch EC2 instance/metric/statistic combo.
- Using matplotlib plot is created and saved on the filesystem.
- Html report is generated allowing preview saved metric plots.
- It will not work for group CloudWatch EC2 instances metrics.

## Audience

Database/ETL developers, Data Integrators, Data Engineers, Business Analysts, AWS Developers, DevOps

## Designated Environment
Pre-Prod (UAT/QA/DEV)

## Usage

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

## Environment variables

```
  set AWS_ACCESS_KEY_ID=<you access key>
  set AWS_SECRET_ACCESS_KEY=<you secret key>
  set AWS_DEFAULT_REGION=<your region > (for example:us-west-2 )
```

# Examples

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

#### Result:

![NetworkIn/Average/10min](https://raw.githubusercontent.com/pydemo/ec2-metrics-plotter/master/plots/EC2_NetworkIn/by_metric/NetworkIn/Average/10/NetworkIn.Average.10.i-fe9cea26.png)

#### Html report
Report is generated with preview for all plots created with this job.
![ALL](https://raw.githubusercontent.com/pydemo/ec2-metrics-plotter/master/plot_reports/networkin.png)



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

#### Result:

![CPUCreditUsage/Average/30min](https://raw.githubusercontent.com/pydemo/ec2-metrics-plotter/master/plots/CPUUtilization/by_instance/i-fe9cea26/1/CPUUtilization.Average.1.i-fe9cea26.png)


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

#### Result:

![CPUCreditUsage/Average/30min](https://raw.githubusercontent.com/pydemo/ec2-metrics-plotter/master/plots/CPUCreditUsage/by_metric/CPUCreditUsage/Average/30/CPUCreditUsage.Average.30.i-fe9cea26.png)


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

#### Result:
One of the plots:
![NetworkIn/Average/10min](https://raw.githubusercontent.com/pydemo/ec2-metrics-plotter/master/plots/CPUCreditBalance/by_instance/i-fe9cea26/30/CPUCreditBalance.Sum.30.i-fe9cea26.png)

#### Html report
Report is generated with preview for all plots created with this job.
![ALL](https://raw.githubusercontent.com/pydemo/ec2-metrics-plotter/master/plot_reports/all.png)


## Download
* [Master Release](https://github.com/pydemo/ec2-metrics-plotter/archive/master.zip) -- `ec2metrics 0.1.0`


#   
# FAQ
#  
#### Can I genereate images of all metrics?
Yes, it is the main purpose of this tool.

#### Can developers integrate `EC2_Metrics_Plotter` into their ETL pipelines?
Yes. Assuming they are doing it on OS Windows.

#### Explain how you generate plots.
I use `matplotlib.pyplot` Python module to do it.
Script is accessing CloudWatch using boto, retrieving metric data and generating plot images.


#### Explain what is included in HTML reports?
Reports include all plot for a given script execution. You can see all plots on one page.

#### Will it work for 2 instances in 2 different regions.
No, you need detailed monitoring to support aggregate statistics.

#### What technology was used to create this tool
I used `Python`, `matplotlib.pyplot`, and `boto3` to write it and `pyInstaller` to compile it in 64-bit windows executable.

#### do you use CloudWatch AWS CLI?
No, I use boto3 to make cals to CloudWatch API.

#### What CloudWatch metrics are included?
This version of Metrics Plotter is tested for EC2 metrics only.
Metrics included:
    CPUUtilization,NetworkIn,NetworkOut,NetworkPacketsIn,
    NetworkPacketsOut,DiskWriteBytes,DiskReadBytes,DiskWriteOps,
    DiskReadOps,CPUCreditBalance,CPUCreditUsage,StatusCheckFailed,
    StatusCheckFailed_Instance,StatusCheckFailed_System
	
#### Does it extract CloudWatch metrics data in csv file?
No

#### Does it use S3 to read metrics?
No, it uses AWS API to read metrics directly from CloudWatch bypassing reports generated on S3.

#### Where are the sources?
Please, contact me for sources.

#### Can you modify functionality and add features?
Yes, please, ask me for new features.

#### What other AWS tools you've created?
- [Oracle_To_S3_Data_Uploader] (https://github.com/pydemo/Oracle_To_S3_Data_Uploader) - Stream Oracle data to Amazon- S3.
- [CSV_Loader_For_Redshift] (https://github.com/pydemo/CSV_Loader_For_Redshift/blob/master/README.md) - Append CSV data to Amazon-Redshift from Windows.
- [S3_Sanity_Check] (https://github.com/pydemo/S3_Sanity_Check/blob/master/README.md) - let's you `ping` Amazon-S3 bucket to see if it's publicly readable.
- [Oracle-To-Redshift-Data-Loader](https://github.com/pydemo/Oracle-To-Redshift-Data-Loader) - plots any CloudWatch EC2 instance  metric stats.
- [S3_File_Uploader](https://github.com/pydemo/S3_File_Uploader/blob/master/README.md) - uploads file from Windows to S3.

#### Do you have any AWS Certifications?
Yes, [AWS Certified Developer (Associate)](https://raw.githubusercontent.com/pydemo/FAQs/master/images/AWS_Ceritied_Developer_Associate.png)

#### Can you create similar/custom data tool for our business?
Yes, you can PM me here or email at `alex_buz@yahoo.com`.
I'll get back to you within hours.

### Links
 - [Employment FAQ](https://github.com/pydemo/FAQs/blob/master/README.md)


[<img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png">](https://www.buymeacoffee.com/0nJ32Xg)
