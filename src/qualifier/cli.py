import click
from prometheus.query_client import QueryClient
from entity.discovery import Discovery
from entity.entity import Entity
from rich.console import Console


@click.command()
@click.option('--host', 'host', required=True, envvar='PROMETHEUS_HOST',
              default='http://localhost:9090', help='The prometheus host to query.')
def cli(host):
    client = QueryClient(host)
    console = Console()

    discovery = Discovery(client)
    entities = discovery.discover()

    console.print('Qualifier Results:\n', style='bold green')

    for entity_type, entity_list in entities.items():
        console.print(f'{entity_type}s:\n', style='bold cyan')

        entity_class = Discovery.entity_classes[entity_type]
        console.print(f'Queries Have Results: {entity_class.query_has_result}', style='bold green')
        console.print(f'Entities Discovered: {entity_class.discovered}\n', style='bold green')

        if not entity_list:
            console.print(f'{entity_type} not discovered', style='bold red')
        for entity in entity_list:
            console.print(f'{entity.name}: {entity.name_labels}', style='bold magenta')
        print('\n')