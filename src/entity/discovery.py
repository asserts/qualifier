import os
from pprint import pprint

from serialize.yamlhandler import read_yaml_file
from entity.entity import Entity
from entity.node import Node
from entity.service import Service


class Discovery:
    entity_classes = {
        'Node': Node,
        'Service': Service
    }

    def __init__(self, client):
        self.client = client
        self.entities = read_yaml_file(
            os.path.join(os.path.dirname(__file__),
                         '../../resources/entities.yml'))
        self.entity_objects = {}

    def discover(self):
        for entity in self.entities['entities']:
            entity_type = entity['type']
            self.entity_objects[entity_type] = {}
            for defined in entity['definedBy']:
                query_result = self.client.instant_query(defined['rawQuery'])

                # query returns a result, check labels against lookup
                if query_result:
                    entity_class = Discovery.entity_classes.get(entity_type)
                    entity_class.entity_query_has_result()

                    name_results = self._get_name(entity['name'], query_result)

                    if name_results:
                        entity_class.entity_discovered()
                        entity_class.set_discovery_queries(defined['id'], defined['sourceQuery'], defined['rawQuery'])
                        for name_value, name_labels in name_results.items():
                            entity_obj = self.entity_objects[entity_type].get(name_value)
                            if entity_obj:
                                entity_obj = self.entity_objects[entity_type][name_value]
                            else:
                                entity_obj = entity_class(entity_type)
                                entity_obj.set_name(name_value)

                            entity_obj.add_name_labels(name_labels)
                            entity_obj.add_query_id(defined['id'])

                            self.entity_objects[entity_type][name_value] = entity_obj

        return self.entity_objects

    def _get_name(self, name, query_result):
        name_results = {}
        tracked_metrics = set()

        possible_labels = [x.strip() for x in name.split('|')]
        for pl in possible_labels:
            for idx, result in enumerate(query_result):
                for label, label_value in result['metric'].items():
                    if label == pl and idx not in tracked_metrics:
                        name_results[label_value] = (pl, label)
                        tracked_metrics.add(idx)

        return name_results

    def _get_lookup(self, lookup, query_result):
        # lookup results is a dict with tuple values
        # where the key is the lookup label_value and the value is the (lookup key, lookup value)
        # e.g. {'api-server', ('workload', 'deployment')}
        lookup_results = {}
        tracked_metrics = set()

        for key, value in lookup.items():
            possible_labels = [x.strip() for x in value.split('|')]
            for pl in possible_labels:
                for idx, result in enumerate(query_result):
                    for label, label_value in result['metric'].items():
                        if label == pl and idx not in tracked_metrics:
                            lookup_results[label_value] = (pl, label)
                            tracked_metrics.add(idx)

        return lookup_results
