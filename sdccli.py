import click

import click
import sdc_cli.utils

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--debug', is_flag=True,
              help='Show debug messages')
def cli(debug):
    if debug:
        print('Set DEBUG in Logging level')


@cli.command('spark')
@click.argument('subcommand')
@click.option('--spark_worker_count', default=1, type=int, help='Number of spark workers?', show_default=True)
@click.option('--spark_worker_cpu', default="1", help='CPU to be allocated per node?', show_default=True)
@click.option('--spark_worker_mem', default="1G", help='RAM to be allocated per node?', show_default=True)
def spark_init(subcommand, spark_worker_count, spark_worker_cpu, spark_worker_mem):
    """
    SUBCOMMANDS AVAILABLE

    \b
        create : Create Spark Cluster with the options provided
        destroy : Destroy the existing spark cluster.

    EXAMPLE:

    \b
        python3 sdccli.py spark create
        python3 sdccli.py spark create --spark_worker_count 2
        python3 sdccli.py spark create --spark_worker_count 2 --spark_worker_cpu=1 --spark_worker_mem=2G
        python3 sdccli.py spark destroy
    """

    if subcommand == 'create':
        sdc_cli.utils.setup_cluster_spark_base(spark_worker_count, spark_worker_cpu, spark_worker_mem)
    elif subcommand == 'destroy':
        sdc_cli.utils.destroy_cluster_spark()
    else:
        print("[er] Subcommand provided does not exist. Please use python3 sdccli.py --help to know supported subcommands")
        exit(1)


@cli.command('cassandra')
@click.argument('subcommand')
@click.option('--cassandra_node', default=1, type=int, help='Number of Nodes?, Default=1', show_default=True)
@click.option('--cassandra_cpu', default="0.5", help='CPU to be allocated per node?', show_default=True)
@click.option('--cassandra_mem', default="2g", help='RAM to be allocated per node?', show_default=True)
def cassandra_init(subcommand, cassandra_node, cassandra_cpu, cassandra_mem):
    """
    SUBCOMMANDS AVAILABLE

    \b
        create : Create Cassandra Cluster with the options provided
        destroy : Destroy the existing Cassandra cluster.


    EXAMPLE:

    \b
        python3 sdccli.py cassandra create
        python3 sdccli.py cassandra create --cassandra_node 2
        python3 sdccli.py cassandra create --cassandra_node 2 --cassandra_cpu=0.7 --cassandra_mem=2g
        python3 sdccli.py cassandra destroy

    """

    if subcommand == 'create':
        sdc_cli.utils.setup_cluster_cassandra_base(cassandra_node, cassandra_cpu, cassandra_mem)
    elif subcommand == 'destroy':
        sdc_cli.utils.destroy_cluster_cassandra()
    else:
        print("[er] Subcommand provided does not exist. Please use python3 sdccli.py --help to know supported subcommands")
        exit(1)


if __name__ == '__main__':
    cli()
