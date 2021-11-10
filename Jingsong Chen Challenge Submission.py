import requests
from collections import defaultdict

node_ids = set()
nodes = {}

# DFS search
def traverseTree(node_id):

    # sanity check - empty node ID
    if not node_id:
        return

    # get node with HTTP request 
    response = requests.get(f'https://nodes-on-nodes-challenge.herokuapp.com/nodes/{node_id}').json()

    # sanity check - multiple nodes associated with a single node ID
    if len(response) != 1:
        print(f'Warning! Multiple nodes associated with ID {node_id}: {response}')
    
    # get & save node
    node = response[0]
    nodes[node['id']] = node['child_node_ids']

    # make node as visited
    node_ids.add(node['id'])

    # grad nodes's children for visit
    for child_id in node['child_node_ids']:
        if child_id not in node_ids:
            traverseTree(child_id)
    
# grab all the nodes
root_id = '089ef556-dfff-4ff2-9733-654645be56fe'
traverseTree(root_id)
print(f'Here are all {len(node_ids)} nodes:', node_ids)

# get the node that's shared the most
shared_counter = defaultdict(int)
for node_id, children in nodes.items():
    for child_id in children:
        if child_id == node_id:
            print(f'Warning! Node {node_id} has itself as a child!')
        else:
            shared_counter[child_id] += 1
shared_counter = sorted(list(shared_counter.items()), key=lambda x: x[1], reverse=True)
print(f'Nodes sorted by the shared count are:', shared_counter)