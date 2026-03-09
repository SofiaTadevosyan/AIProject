import os
import sqlite3
import sys
from owlready2 import *
import re

# Fixed SyntaxWarning: using raw string for Windows path
owlready2.JAVA_EXE = r"C:\Program Files\Java\jdk-25\bin\java.exe"

# 1. SETUP PATHS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ONTO_FILE = os.path.join(BASE_DIR, "Botany.rdf")
DB_FILE = os.path.join(BASE_DIR, "botany_entities.db")

# ===== REMOVE WebProtégé URN IMPORTS (prevents load crash) =====
def make_imports_safe_copy(src_path: str) -> str:
    if not os.path.exists(src_path):
        print(f"❌ File not found: {src_path}")
        sys.exit(1)
    with open(src_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    text = re.sub(r'<owl:imports[^>]*?/>\s*', '', text)
    text = re.sub(r'<owl:imports\b[^>]*>\s*</owl:imports>\s*', '', text)
    safe_path = os.path.join(os.path.dirname(src_path), "Botany.rdf")
    with open(safe_path, "w", encoding="utf-8") as f:
        f.write(text)
    return safe_path

# ===== LOAD ONTOLOGY =====
try:
    safe_onto_path = make_imports_safe_copy(ONTO_FILE)
    onto = get_ontology(safe_onto_path).load()
    # Get the namespace of the loaded ontology to help finding entities
    # This targets the 'untitled-ontology-3' namespace from your screenshot
    ns = onto.get_namespace(onto.base_iri)
    print(f"✅ Botany Ontology Loaded. Base IRI: {onto.base_iri}")
except Exception as e:
    print(f"❌ Load Error: {e}")
    sys.exit(1)

# ===== NAMESPACE-AWARE ENTITY FINDER =====
def find_entity(name):
    # Method 1: Search within the specific ontology namespace (Best)
    ent = ns[name]
    # Method 2: Global IRI search if Method 1 fails
    if not ent:
        ent = onto.search_one(iri=f"*{name}")
    # Method 3: Search by Label
    if not ent:
        ent = onto.search_one(label=name)
    return ent

def prop_attr(prop):
    if prop is None: return None
    return getattr(prop, "python_name", None) or prop.name

# ===== MAPPING ENTITIES (Based on your screenshots) =====
PlantClass            = find_entity("Plant")
HabitatClass          = find_entity("Habitat")
GeographicRegionClass = find_entity("GeographicRegion")
# Object Properties
foundInHabitat        = find_entity("foundInHabitat")
isNativeToRegion      = find_entity("isNativeToRegion")
# Data Properties
hasMaxLatitude        = find_entity("hasMaxLatitude")
hasMinLatitude        = find_entity("hasMinLatitude")

# Validation check
entities_to_check = {
    "Plant": PlantClass,
    "Habitat": HabitatClass,
    "foundInHabitat": foundInHabitat,
    "isNativeToRegion": isNativeToRegion
}

missing = [name for name, obj in entities_to_check.items() if obj is None]
if missing:
    print(f"❌ Still missing: {', '.join(missing)}")
    print("\nDEBUG INFO:")
    print("Listing all classes found in file:")
    print(list(onto.classes()))
    sys.exit(1)

print("🎯 All Botany entities mapped successfully.")

# ===== DATABASE TO ONTOLOGY MAPPING =====
try:
    if not os.path.exists(DB_FILE):
        print(f"❌ Database file not found: {DB_FILE}")
        sys.exit(1)
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    with onto:
        # 1. Map Habitats (Assume DB table 'Habitat' has 'id')
        habitats = {}
        try:
            cursor.execute("SELECT id FROM Habitat")
            for (h_id,) in cursor.fetchall():
                ind = HabitatClass(f"Habitat_{h_id}")
                habitats[h_id] = ind
        except sqlite3.Error as e:
            print(f"⚠️ Habitat table skip: {e}")

        # 2. Map Regions
        regions = {}
        try:
            cursor.execute("SELECT id FROM GeographicRegion")
            for (r_id,) in cursor.fetchall():
                ind = GeographicRegionClass(f"Region_{r_id}")
                regions[r_id] = ind
        except sqlite3.Error as e:
            print(f"⚠️ Region table skip: {e}")

        # 3. Map Plants and link them
        # Adjust column names (id, habitat_id, region_id) to match your DB exactly
        cursor.execute("SELECT id, habitat_id, region_id, max_lat, min_lat FROM Plant")
        for p_id, h_id, r_id, max_lat, min_lat in cursor.fetchall():
            p_ind = PlantClass(f"Plant_{p_id}")
            
            # Link to Habitat
            if h_id in habitats and foundInHabitat:
                getattr(p_ind, prop_attr(foundInHabitat)).append(habitats[h_id])
            
            # Link to Region
            if r_id in regions and isNativeToRegion:
                getattr(p_ind, prop_attr(isNativeToRegion)).append(regions[r_id])

            # Data Properties
            if max_lat is not None and hasMaxLatitude:
                setattr(p_ind, prop_attr(hasMaxLatitude), [float(max_lat)])
            if min_lat is not None and hasMinLatitude:
                setattr(p_ind, prop_attr(hasMinLatitude), [float(min_lat)])

    conn.close()
    print("📥 Data mapping complete.")

except Exception as e:
    print(f"❌ Processing Error: {e}")
    sys.exit(1)

# ===== RUN REASONER =====
print("🧠 Reasoning...")
try:
    sync_reasoner(infer_property_values=True)
    print("✨ Complete!")
except Exception as e:
    print(f"⚠️ Reasoner issue: {e}")

# ===== SAVE =====
out_path = os.path.join(BASE_DIR, "botany_final.owl")
onto.save(file=out_path, format="rdfxml")
print(f"💾 Saved to: {out_path}")