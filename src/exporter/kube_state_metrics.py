class KubeStateMetrics:

    queries = [
        'kube_node_info',
        'count without (instance, container, uid)(kube_pod_owner)',
        'count by(pod, namespace, node)(kube_pod_info)',
    ]

    def __init__(self, client):
        self.client = client
        self.standalone_job = False

