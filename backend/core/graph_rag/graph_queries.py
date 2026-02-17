"""Cypher query templates for GraphRAG."""


class GraphQueries:
    FULL_CONTEXT = """
    MATCH path = (d)-[:AFFECTS*1..3]-(entity)
    WHERE d.name = $disaster OR d.type = $disaster
    RETURN [n IN nodes(path) | {name: n.name, labels: labels(n)}] AS path_nodes,
           [r IN relationships(path) | type(r)] AS rel_types
    LIMIT 30
    """

    AFFECTED_ENTITIES = """
    MATCH (l:Location {name: $location})<-[:LOCATED_IN]-(entity)
    RETURN entity.name AS name, labels(entity)[0] AS type,
           entity.criticality AS criticality
    LIMIT 30
    """

    EVACUATION_ROUTES = """
    MATCH (src:Location {name: $from})-[:CONNECTED_TO*1..4]-(dest:Location)
    WHERE NOT EXISTS((dest)<-[:AFFECTS]-(:Flood))
    RETURN dest.name AS safe_location,
           length(shortestPath((src)-[:CONNECTED_TO*]-(dest))) AS hops
    ORDER BY hops LIMIT 10
    """

    DEPENDENT_SERVICES = """
    MATCH (infra {name: $infra_name})<-[:DEPENDS_ON]-(svc)
    RETURN svc.name AS service, labels(svc)[0] AS type, svc.criticality AS criticality
    """

    RISK_PATHS = """
    MATCH (disaster)-[:AFFECTS]->(infra)-[:DEPENDS_ON]->(critical)
    WHERE disaster.name = $disaster_type
    RETURN disaster.name AS disaster, infra.name AS infrastructure,
           critical.name AS critical_dependency
    LIMIT 20
    """
