# Implementing custom magics

from IPython.core.magic import (register_line_magic, register_cell_magic, register_line_cell_magic)
from pyspark import SparkContext,SparkConf
import os

# This is the JupyterHub login username 
# (it might not correspond to the OS username, 
# which is tipycally Jovyan)
def user():
   
    path=os.environ['JUPYTERHUB_SERVICE_PREFIX']
    path_list = path.split(os.sep)
    username=path_list[2]
    
    return username

@register_line_magic
def login_user(self):
    
    username=user()
    
    return username

# Define the Spark context
@register_line_magic
def sc(num_workers):
    
    # set default number of workers
    if not num_workers:
        num_workers=25
    # ser max number of workers 
    max_workers=25
    #if int(num_workers) > max_workers:
    #    num_workers=max_workers
        
    username=user()
    
    sconf=SparkConf()
    # add sparkmonitor extension
    sconf.set("spark.extraListeners", "sparkmonitor.listener.JupyterSparkMonitorListener")
    sconf.set("spark.driver.extraClassPath","/opt/conda/lib/python3.7/site-packages/sparkmonitor/listener.jar")
    sconf.set("spark.master", "k8s://https://192.168.2.39:6443")
    sconf.set("spark.name", "spark-"+username)
    sconf.set("spark.submit.deployMode", "client")
    sconf.set("spark.kubernetes.namespace", username)
    sconf.set("spark.executor.instances", num_workers)
    sconf.set("spark.kubernetes.container.image", "svallero/spark:2.4.3-2")
    sconf.set("spark.driver.host", "jupyter-"+username+".jhub.svc.cluster.local")
    #sconf.set("spark.driver.host", "192.168.149.9")
    sconf.set('spark.app.name', "jupyter-"+username)
    sconf.set('spark.kubernetes.pyspark.pythonVersion', "3")
    sconf.set("spark.driver.port", 34782)
    sconf.set("spark.executorEnv.HADOOP_USER_NAME", "jovyan")
    sconf.set("spark.driver.memory", "10g")
    sconf.set("spark.executor.memory", "10g")
    sconf.set("spark.executor.cores", "5") # magic number to achieve maximum HDFS throughtput   
    
    context=SparkContext(conf=sconf)   
    context.setLogLevel("DEBUG")
    context._conf.getAll()
    
    return context

# Define the Spark context
@register_line_magic
def sc_test(num_workers):
    
    username=user()
    
    #print('Num workers '+num_workers)
    
    sconf=SparkConf()
    # add sparkmonitor extension
    sconf.set("spark.extraListeners", "sparkmonitor.listener.JupyterSparkMonitorListener")
    #add jars for BigDL and analytics zoo
    sconf.set("spark.driver.extraClassPath","/opt/conda/lib/python3.7/site-packages/sparkmonitor/listener.jar:/opt/conda/lib/python3.7/site-packages/bigdl/share/lib/bigdl-0.9.0-jar-with-dependencies.jar:/opt/conda/lib/python3.7/site-packages/zoo/share/lib/analytics-zoo-bigdl_0.9.1-spark_2.4.3-0.6.0-jar-with-dependencies.jar")
    sconf.set("spark.jars","/opt/conda/lib/python3.7/site-packages/bigdl/share/lib/bigdl-0.9.0-jar-with-dependencies.jar,/opt/conda/lib/python3.7/site-packages/zoo/share/lib/analytics-zoo-bigdl_0.9.1-spark_2.4.3-0.6.0-jar-with-dependencies.jar")
    sconf.set("spark.executor.extraClassPath","/opt/conda/lib/python3.7/site-packages/bigdl/share/lib/bigdl-0.9.0-jar-with-dependencies.jar:/opt/conda/lib/python3.7/site-packages/zoo/share/lib/analytics-zoo-bigdl_0.9.1-spark_2.4.3-0.6.0-jar-with-dependencies.jar")
    sconf.set("spark.master", "k8s://https://192.168.2.39:6443")
    sconf.set("spark.name", "spark-"+username)
    sconf.set("spark.submit.deployMode", "client")
    sconf.set("spark.kubernetes.namespace", username)
    sconf.set("spark.executor.instances", num_workers)
    sconf.set("spark.kubernetes.container.image", "svallero/spark:2.4.3-2")
    sconf.set("spark.driver.host", "jupyter-"+username+".jhub.svc.cluster.local")
    #sconf.set("spark.driver.host", "192.168.149.9")
    sconf.set('spark.app.name', "jupyter-"+username)
    sconf.set('spark.kubernetes.pyspark.pythonVersion', "3")
    sconf.set("spark.driver.port", 34782)
    sconf.set("spark.executorEnv.HADOOP_USER_NAME", "jovyan")
    sconf.set("spark.driver.memory", "10g")
    sconf.set("spark.executor.memory", "10g")

    sconf.set("spark.executor.cores", "5") # magic number to achieve maximum HDFS throughtput
    #sconf.set("spark.kubernetes.node.selector.kubernetes.io/hostname","t2-mlwn-02.to.infn.it")    
    sconf.set("spark.kubernetes.node.selector.cluster", "t2-mlwn")
    
    context=SparkContext(conf=sconf)   
    context.setLogLevel("DEBUG")
    context._conf.getAll()
    
    return context

# Define the Spark context for bigDL
@register_line_magic
def sc_bigDL(num_workers):
    
    # set default number of workers
    if not num_workers:
        num_workers=25
    # ser max number of workers 
    max_workers=25
    #if int(num_workers) > max_workers:
    #    num_workers=max_workers
        
    username=user()
    
    #print('Num workers '+num_workers)
    
    sconf=SparkConf()
    # add sparkmonitor extension
    sconf.set("spark.extraListeners", "sparkmonitor.listener.JupyterSparkMonitorListener")
    #add jars for BigDL and analytics zoo
    sconf.set("spark.driver.extraClassPath","/opt/conda/lib/python3.7/site-packages/sparkmonitor/listener.jar:/opt/conda/lib/python3.7/site-packages/bigdl/share/lib/bigdl-0.9.0-jar-with-dependencies.jar:/opt/conda/lib/python3.7/site-packages/zoo/share/lib/analytics-zoo-bigdl_0.9.1-spark_2.4.3-0.6.0-jar-with-dependencies.jar")
    sconf.set("spark.jars","/opt/conda/lib/python3.7/site-packages/bigdl/share/lib/bigdl-0.9.0-jar-with-dependencies.jar,/opt/conda/lib/python3.7/site-packages/zoo/share/lib/analytics-zoo-bigdl_0.9.1-spark_2.4.3-0.6.0-jar-with-dependencies.jar")
    sconf.set("spark.executor.extraClassPath","/opt/conda/lib/python3.7/site-packages/bigdl/share/lib/bigdl-0.9.0-jar-with-dependencies.jar:/opt/conda/lib/python3.7/site-packages/zoo/share/lib/analytics-zoo-bigdl_0.9.1-spark_2.4.3-0.6.0-jar-with-dependencies.jar")
    sconf.set("spark.master", "k8s://https://192.168.2.39:6443")
    sconf.set("spark.name", "spark-"+username)
    sconf.set("spark.submit.deployMode", "client")
    sconf.set("spark.kubernetes.namespace", username)
    sconf.set("spark.executor.instances", num_workers)
    sconf.set("spark.kubernetes.container.image", "svallero/spark:2.4.3-2")
    sconf.set("spark.driver.host", "jupyter-"+username+".jhub.svc.cluster.local")
    #sconf.set("spark.driver.host", "192.168.149.9")
    sconf.set('spark.app.name', "jupyter-"+username)
    sconf.set('spark.kubernetes.pyspark.pythonVersion', "3")
    sconf.set("spark.driver.port", 34782)
    sconf.set("spark.executorEnv.HADOOP_USER_NAME", "jovyan")
    sconf.set("spark.driver.memory", "10g")
    sconf.set("spark.executor.memory", "10g")   
    
    #for bigDL, check these settings
    sconf.set("spark.executor.cores", "1")
    sconf.set("spark.cores.max", "1")
    sconf.set("spark.shuffle.reduceLocality.enabled", "false")
    sconf.set("spark.shuffle.blockTransferService", "nio")
    sconf.set("spark.scheduler.minRegisteredResourcesRatio", "1.0")
    sconf.set("spark.speculation", "false")    
    
    context=SparkContext(conf=sconf)   
    context.setLogLevel("DEBUG")
    context._conf.getAll()
    
    return context

# Path to the user's home dir on HDFS
@register_line_magic
def hdfs_path(self):
    
    username=user()
    path="hdfs://192.168.2.39/user/"+username
    
    return path
    
