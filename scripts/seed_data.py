"""Run all seed scripts."""
import subprocess
subprocess.run(["python", "scripts/init_neo4j.py"])
subprocess.run(["python", "scripts/init_qdrant.py"])
print("All seed data loaded.")
