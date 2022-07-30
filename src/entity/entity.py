class Entity:
    names = []
    query_has_result = False
    discovered = False
    discovery_queries = {}

    def __init__(self, type):
        self.type = type
        self.name = None
        self.name_labels = []
        self.query_ids = []

    def set_name(self, name):
        self.name = name
        Entity.names.append(name)

    def add_name_labels(self, name_labels):
        self.name_labels.append(name_labels)

    def add_query_id(self, query_id):
        self.query_ids.append(query_id)

    def get_class(self):
        return self.__class__

    @classmethod
    def entity_query_has_result(cls):
        cls.query_has_result = True

    @classmethod
    def entity_discovered(cls):
        cls.discovered = True

    @classmethod
    def set_discovery_queries(cls, idx, source_query, raw_query):
        if cls.discovery_queries.get(idx):
            cls.discovery_queries[idx].append((source_query, raw_query))
        else:
            cls.discovery_queries[idx] = [(source_query, raw_query)]
