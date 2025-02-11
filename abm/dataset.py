from common import connect, GALAXY_SERVER
from pprint import pprint
import yaml

def list(args: list):
    gi = connect()
    datasets = gi.datasets.get_datasets(limit=10000, offset=0)  # , deleted=True, purged=True)
    if len(datasets) == 0:
        print('No datasets found')
        return
    print(f'Found {len(datasets)} datasets')
    print('ID\tDeleted\tState\tName')
    for dataset in datasets:
        state = dataset['state'] if 'state' in dataset else 'unknown'
        print(f"{dataset['id']}\t{dataset['deleted']}\t{state}\t{dataset['name']}")
        # pprint(dataset)

def clean(args: list):
    if len(args) == 0:
        invalid_states = ['error', 'discarded', 'unknown']
    else:
        invalid_states = args
    gi = connect()
    datasets = gi.datasets.get_datasets(limit=10000, offset=0)  # , deleted=True, purged=True)
    if len(datasets) == 0:
        print('No datasets found')
        return
    for dataset in datasets:
        state = dataset['state'] if 'state' in dataset else 'unknown'
        if not dataset['deleted'] and state in invalid_states:
            gi.histories.delete_dataset(dataset['history_id'], dataset['id'], True)
            print(f"Removed {dataset['id']}\t{state}\t{dataset['name']}")

def show(args: list):
    if len(args) == 0:
        print("ERROR: no dataset ID provided")
        return
    gi = connect()
    pprint(gi.datasets.show_dataset(args[0]))

def delete(args: list):
    gi = connect()
    print("dataset delete not implemented")

def upload(args: list):
    gi = connect()
    if len(args) == 0:
        print('ERROR: no dataset file given')
        return
    else:
        index = 1
        while index < len(args):
            arg = args[index]
            index += 1
            if arg == '-id':
                history = args[index]
                index += 1
            elif arg == '-c':
                history = gi.histories.create_history(args[index]).get('id')
                index += 1
            else:
                print('ERROR: invalid option')
    pprint(gi.tools.put_url(args[0], history))


def download(args: list):
    gi = connect()
    if len(args) == 0:
        print('ERROR: no dataset ID given')
        return
    elif len(args) > 1:
        pprint(gi.datasets.download_dataset(args[0], file_path=args[1]))
    else:
        pprint(gi.datasets.download_dataset(args[0]))


def find(args: list):
    if len(args) == 0:
        print('ERROR: now dataset name given.')
        return
    gi = connect()
    datasets = gi.datasets.get_datasets(name=args[0])
    if len(datasets) == 0:
        print('WARNING: no datasets found with that name')
        return
    if len(datasets) > 1:
        print(f'WARNING: found {len(datasets)} datasets with that name. Using the first')
        print('dataset in the list. Which one that is will be indeterminate.')

    ds = datasets[0]
    pprint(ds)


def test(args: list):
    if len(args) == 0:
        print("ERROR: no dataset ID provided")
        return
    gi = connect()
    dataset = gi.datasets.show_dataset(args[0])
    if dataset is None:
        print(f"ERROR: no dataset with ID {args[0]}")
        return
    name = dataset['name']
    print(f"Found dataset with name {name}")
    print(yaml.dump(dataset))
    datasets = gi.datasets.get_datasets(name=name)
    if datasets is None or len(datasets) == 0:
        print(f"ERROR: could not find a dataset named {name}")
        return
    print(f"Found {len(datasets)} datasets")
    for dataset in datasets:
        print(f"{dataset['id']}\t{dataset['name']}")
