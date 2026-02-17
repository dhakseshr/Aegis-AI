"""Neo4j GraphRAG client."""
from neo4j import GraphDatabase
from typing import List, Dict, Any
import os


class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "aegisai123"))
        )

    def run_query(self, query: str, params: Dict = None) -> List[Dict]:
        with self.driver.session() as session:
            result = session.run(query, params or {})
            return [dict(r) for r in result]

    def get_infrastructure_risks(self, location: str, disaster_type: str) -> List[Dict]:
        query = """
        MATCH (d {name: $disaster_type})-[:AFFECTS]->(infra)
        WHERE infra.location = $location OR infra.city = $location
        RETURN infra.name AS name, infra.type AS type,
               infra.criticality AS criticality, infra.status AS status
        ORDER BY infra.criticality DESC LIMIT 20
        """
        return self.run_query(query, {"disaster_type": disaster_type, "location": location})

    def get_nearby_resources(self, location: str) -> List[Dict]:
        query = """
        MATCH (l:Location {name: $location})-[:NEARBY|LOCATED_IN*1..2]-(r)
        WHERE r:Hospital OR r:Shelter OR r:EmergencyService
        RETURN r.name AS name, labels(r)[0] AS type,
               r.capacity AS capacity, r.contact AS contact
        LIMIT 20
        """
        return self.run_query(query, {"location": location})

    def seed_sample_data(self):
        """Seed Chennai disaster scenario."""
        with self.driver.session() as session:
            session.run("""
            MERGE (chennai:Location {name: 'Chennai', state: 'Tamil Nadu', country: 'India'})
            MERGE (flood:Flood {name: 'Flood', type: 'natural_disaster'})
            MERGE (h1:Hospital {name: 'Rajiv Gandhi Govt Hospital', capacity: 1500, city: 'Chennai', contact: '044-25305000'})
            MERGE (h2:Hospital {name: 'Stanley Medical College', capacity: 1200, city: 'Chennai', contact: '044-25281349'})
            MERGE (s1:Shelter {name: 'Chennai Corporation School Shelter', capacity: 500, city: 'Chennai'})
            MERGE (s2:Shelter {name: 'Anna University Relief Camp', capacity: 800, city: 'Chennai'})
            MERGE (r1:Road {name: 'NH32 Chennai-Kolkata Highway', status: 'at_risk', criticality: 'high'})
            MERGE (pg:PowerGrid {name: 'Metrowater Power Station', criticality: 'critical', city: 'Chennai'})
            MERGE (es:EmergencyService {name: 'NDRF Chennai', contact: '1078', type: 'rescue'})

            MERGE (flood)-[:AFFECTS]->(h1)
            MERGE (flood)-[:AFFECTS]->(r1)
            MERGE (flood)-[:AFFECTS]->(pg)
            MERGE (h1)-[:LOCATED_IN]->(chennai)
            MERGE (h2)-[:LOCATED_IN]->(chennai)
            MERGE (s1)-[:LOCATED_IN]->(chennai)
            MERGE (s2)-[:LOCATED_IN]->(chennai)
            MERGE (es)-[:SERVES]->(chennai)
            MERGE (s1)-[:NEARBY]->(h1)
            MERGE (pg)-[:DEPENDS_ON]->(r1)
            MERGE (chennai)-[:CONNECTED_TO]->(:Location {name: 'Kancheepuram'})
            """)

    def close(self):
        self.driver.close()
