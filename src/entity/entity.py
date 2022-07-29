class Entity:
    query_has_result = False
    discovered = False
    discovery_queries = []

    def __init__(self, type):
        self.type = type
        self.name = None
        self.name_labels = None

    def set_name(self, name):
        self.name = name

    def set_name_labels(self, name_labels):
        self.name_labels = name_labels

    def get_class(self):
        return self.__class__

    @classmethod
    def entity_query_has_result(cls):
        cls.query_has_result = True

    @classmethod
    def entity_discovered(cls):
        cls.discovered = True

    @classmethod
    def set_discovery_queries(cls, source_query, raw_query):
        if cls.discovery_queries:
            cls.discovery_queries.append((source_query, raw_query))
        else:
            cls.discovery_queries = [(source_query, raw_query)]
