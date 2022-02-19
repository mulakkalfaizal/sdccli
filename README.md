# sdccli

CLI tool will help set up or destroy a development environment for the Cassandra cluster and spark cluster

## Prerequisites
* Python3
* Docker
* Docker Compose

## Install
```shell script
git clone git@github.com:mulakkalfaizal/sdccli.git
cd sdccli
python3 -m venv ./venv
pip3 install -r requirements.txt
```

## Verify
```shell
python3 sdccli.py 
```
### Command output
```shell
# python3 sdccli.py              
Usage: sdccli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --debug     Show debug messages
  -h, --help  Show this message and exit.

Commands:
  cassandra  SUBCOMMANDS AVAILABLE
  spark      SUBCOMMANDS AVAILABLE
 
```

## Usage

### Commands Available
* cassandra
* spark

### Command Output
```text
# python3 sdccli.py --help
Usage: sdccli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --debug     Show debug messages
  -h, --help  Show this message and exit.

Commands:
  cassandra  SUBCOMMANDS AVAILABLE
  spark      SUBCOMMANDS AVAILABLE
```

## Create Spark Cluster

### Create a spark cluster with default configuration
```shell
python3 sdccli.py spark create
```
### Command Output
```text
# python3 sdccli.py spark create

[i] Saving file : ./spark_home/docker-compose.yaml
[i] File saved : ./spark_home/docker-compose.yaml
[i] Starting docker compose for spark
Creating network "spark_home_default" with the default driver
Creating spark_home_spark-worker_1 ... done
Creating spark_home_spark-master_1 ... done
spark_home_spark-master_1 is up-to-date
spark_home_spark-worker_1 is up-to-date
[i] Installing the datastax connector...
Ivy Default Cache set to: /root/.ivy2/cache
The jars for the packages stored in: /root/.ivy2/jars
:: loading settings :: url = jar:file:/opt/bitnami/spark/jars/ivy-2.4.0.jar!/org/apache/ivy/core/settings/ivysettings.xml
com.datastax.spark#spark-cassandra-connector_2.12 added as a dependency
:: resolving dependencies :: org.apache.spark#spark-submit-parent-41a1ce39-70fd-4904-abfa-73f981370b60;1.0
	confs: [default]
	found com.datastax.spark#spark-cassandra-connector_2.12;3.0.0 in central
	found com.datastax.spark#spark-cassandra-connector-driver_2.12;3.0.0 in central
	found com.datastax.oss#java-driver-core-shaded;4.7.2 in central
	found com.datastax.oss#native-protocol;1.4.10 in central
	....
	....
[i] Spark Cluster is ready to use
SPARK MASTER URL : http://localhost:8080
```
### Get help to create spark cluster
```text
# python3 sdccli.py spark --help 

Usage: sdccli.py spark [OPTIONS] SUBCOMMAND

  SUBCOMMANDS AVAILABLE

      create : Create Spark Cluster with the options provided
      destroy : Destroy the existing spark cluster.

  EXAMPLE:

      python3 sdccli.py spark create
      python3 sdccli.py spark create --spark_worker_count 2
      python3 sdccli.py spark create --spark_worker_count 2 --spark_worker_cpu=1 --spark_worker_mem=2G
      python3 sdccli.py spark destroy

Options:
  --spark_worker_count INTEGER  Number of spark workers?  [default: 1]
  --spark_worker_cpu TEXT       CPU to be allocated per node?  [default: 1]
  --spark_worker_mem TEXT       RAM to be allocated per node?  [default: 1G]
  -h, --help                    Show this message and exit.
```

## Create Cassandra Cluster

### Create a Cassandra cluster with default configuration
```shell
python3 sdccli.py Cassandra create
```
### Command Output
```text
# python3 sdccli.py cassandra create

[i] Saving file : cassandra_home/docker-compose.yaml
[i] File saved : cassandra_home/docker-compose.yaml
[i] Starting docker compose for Cassandra
Creating network "cassandra_home_cassandra" with the default driver
Creating cassandra1 ... done
[i] Cassandra Cluster is ready
```

### Get help to create Cassandra cluster
```text
# python3 sdccli.py cassandra --help

Usage: sdccli.py cassandra [OPTIONS] SUBCOMMAND

  SUBCOMMANDS AVAILABLE

      create : Create Cassandra Cluster with the options provided
      destroy : Destroy the existing Cassandra cluster.

  EXAMPLE:

      python3 sdccli.py cassandra create
      python3 sdccli.py cassandra create --cassandra_node 2
      python3 sdccli.py cassandra create --cassandra_node 2 --cassandra_cpu=0.7 --cassandra_mem=200m
      python3 sdccli.py cassandra destroy

Options:
  --cassandra_node INTEGER  Number of Nodes?, Default=1  [default: 1]
  --cassandra_cpu TEXT      CPU to be allocated per node?  [default: 0.5]
  --cassandra_mem TEXT      RAM to be allocated per node?  [default: 2g]
  -h, --help                Show this message and exit.
```

## Destroy Spark Cluster
```shell
python3 sdccli.py spark destroy
```
### Command Output
```text
# python3 sdccli.py spark destroy

[i] Destroying the spark cluster
[!] Are you sure you want to proceed? (y/n): y
Stopping spark_home_spark-master_1 ... done
Stopping spark_home_spark-worker_1 ... done
Removing spark_home_spark-master_1 ... done
Removing spark_home_spark-worker_1 ... done
Removing network spark_home_default
[i] Spark cluster is destroyed
```

## Destroy Cassandra Cluster
```shell
python3 sdccli.py cassandra destroy
```

### Command Output
```text
# python3 sdccli.py cassandra destroy

[i] Destroying Cassandra cluster
[!] Are you sure you want to proceed? (y/n): y
Stopping cassandra1 ... done
Removing cassandra1 ... done
Removing network cassandra_home_cassandra
[i] Cassandra cluster is destroyed
```

