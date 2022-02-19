import os
import conf

try:
    from ruamel import yaml
except ImportError:
    import yaml


def confirm_prompt(question: str) -> bool:
    reply = None
    while reply not in ("y", "n"):
        reply = input(f"{question} (y/n): ").lower()
    return reply == "y"


def generate_cassandra_compose_dict(name, image, node_number, mem, cpu):
    node_name = f'{name}{node_number}'
    starting_port_number = 9040
    entry = {'image': image,
             'container_name': node_name,
             'hostname': node_name,
             'mem_limit': mem,
             'cpus': cpu,
             'healthcheck': {
                 'test': ["CMD", "cqlsh", "-e", "describe keyspaces"],
                 'interval': '5s',
                 'timeout': '10s',
                 'retries': 60
             },
             'networks': ['cassandra'],
             'ports': [f'{starting_port_number + node_number}:9042'],
             'volumes': [f'./data2/cassandra{node_number}:/var/lib/cassandra'],
             'environment': {
                 'CASSANDRA_SEEDS': "cassandra1",
                 'CASSANDRA_CLUSTER_NAME': "sdc-cluster"
             }
             }
    if not node_name == 'cassandra1':
        entry['depends_on'] = {f'cassandra{node_number - 1}': {'condition': 'service_healthy'}}
    # print(entry)
    return entry


def generate_spark_compose_dict(name, image, mem, cpu):
    entry = {'image': image,
             }
    if name.endswith("master"):
        entry['ports'] = ['8080:8080']
        entry['environment'] = {
            'SPARK_MODE': "master",
            'SPARK_RPC_AUTHENTICATION_ENABLED': 'no',
            'SPARK_RPC_ENCRYPTION_ENABLED': 'no',
            'SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED': 'no',
            'SPARK_SSL_ENABLED': 'no'
             }
        entry['user'] = 'root'

    else:
        entry['environment'] = {
            'SPARK_MODE': 'worker',
            'SPARK_MASTER_URL': 'spark://spark-master:7077',
            'SPARK_WORKER_MEMORY': mem,
            'SPARK_WORKER_CORES': cpu,
            'SPARK_RPC_AUTHENTICATION_ENABLED': 'no',
            'SPARK_RPC_ENCRYPTION_ENABLED': 'no',
            'SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED': 'no',
            'SPARK_SSL_ENABLED': 'no',
        }
    # print(entry)
    return entry


def save_file(file_name, file_data):
    print(f"[i] Saving file : {file_name}")
    with open(f"{file_name}", "w") as file:
        file.write(file_data)
    print(f"[i] File saved : {file_name} ")


def setup_cluster_cassandra_base(node_count, node_cpu, node_mem):
    cassandra_home = "cassandra_home"
    cassandra_dc_file = f'./{cassandra_home}/docker-compose.yaml'

    if not os.path.exists(cassandra_home):
        os.makedirs(cassandra_home)

    cassandra_services = {
        'cassandra': conf.CASSANDRA_IMAGE
    }

    cassandra_composition = {'services': {}, 'version': '2.4', 'networks': {'cassandra': {}}}

    for i in range(1, node_count + 1):
        for name, image in cassandra_services.items():
            cassandra_composition['services'][f"{name}{i}"] = generate_cassandra_compose_dict(name, image, i, node_mem, node_cpu)
    #print(yaml.dump(cassandra_composition, default_flow_style=False, indent=4), end='')

    save_file(f'{cassandra_home}/docker-compose.yaml', yaml.dump(cassandra_composition, default_flow_style=False, indent=4))

    print("[i] Starting docker compose for Cassandra")
    os.system(f'docker-compose -f {cassandra_dc_file} up -d')
    print("[i] Cassandra Cluster is ready")


def setup_cluster_spark_base(worker_count, node_cpu, node_mem):
    spark_home = "spark_home"
    spark_dc_file = f'./{spark_home}/docker-compose.yaml'
    spark_master = 'spark_home_spark-master_1'
    spark_cassandra_connector = conf.SPARK_CASSANDRA_CONNECTOR

    if not os.path.exists(spark_home):
        os.makedirs(spark_home)

    spark_services = {
        'spark-master': conf.SPARK_MASTER_IMAGE,
        'spark-worker': conf.SPARK_WORKER_IMAGE
    }

    spark_composition = {'services': {}, 'version': '2.4'}

    for name, image in spark_services.items():
        spark_composition['services'][name] = generate_spark_compose_dict(name, image, node_mem, node_cpu)
    #print(yaml.dump(spark_composition, default_flow_style=False, indent=4), end='')

    save_file(spark_dc_file, yaml.dump(spark_composition, default_flow_style=False, indent=4))

    print("[i] Starting docker compose for spark")
    os.system(f'docker-compose -f {spark_dc_file} up -d')
    if worker_count:
        os.system(f'docker-compose -f {spark_dc_file} up --scale spark-worker={worker_count} -d')

    print("[i] Installing the datastax connector...")
    os.system(f'docker exec -it {spark_master} /bin/bash ./bin/spark-shell --packages {spark_cassandra_connector}')

    print("[i] Spark Cluster is ready to use \nSPARK MASTER URL : http://localhost:8080")


def destroy_cluster_spark():
    print("[i] Destroying the spark cluster")
    spark_home = "spark_home"
    user_response = confirm_prompt("[!] Are you sure you want to proceed?")
    if user_response:
        spark_dc_file = f'./{spark_home}/docker-compose.yaml'
        os.system(f'docker-compose -f {spark_dc_file} down')
        print("[i] Spark cluster is destroyed")
    else:
        print("[i] Safely exiting.. No changes")


def destroy_cluster_cassandra():
    print("[i] Destroying Cassandra cluster")
    cassandra_home = "cassandra_home"
    user_response = confirm_prompt("[!] Are you sure you want to proceed?")
    if user_response:
        cassandra_dc_file = f'./{cassandra_home}/docker-compose.yaml'
        os.system(f'docker-compose -f {cassandra_dc_file} down')
        print("[i] Cassandra cluster is destroyed")
    else:
        print("[i] Safely exiting.. No changes")