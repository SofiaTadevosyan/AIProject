import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "botany_entities.db")

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create Tables based on your Ontology hierarchy
cursor.executescript('''
    CREATE TABLE IF NOT EXISTS Habitat (
        id INTEGER PRIMARY KEY,
        name TEXT
    );

    CREATE TABLE IF NOT EXISTS GeographicRegion (
        id INTEGER PRIMARY KEY,
        name TEXT
    );

    CREATE TABLE IF NOT EXISTS Plant (
        id INTEGER PRIMARY KEY,
        name TEXT,
        habitat_id INTEGER,
        region_id INTEGER,
        max_lat REAL,
        min_lat REAL,
        FOREIGN KEY (habitat_id) REFERENCES Habitat(id),
        FOREIGN KEY (region_id) REFERENCES GeographicRegion(id)
    );

    -- Optional: Add some sample data to test
    INSERT OR IGNORE INTO Habitat (id, name) VALUES (1, 'Desert');
    INSERT OR IGNORE INTO GeographicRegion (id, name) VALUES (1, 'Sahara');
    INSERT OR IGNORE INTO Plant (id, name, habitat_id, region_id, max_lat, min_lat) 
    VALUES (1, 'Cactus', 1, 1, 35.0, 15.0);
''')

conn.commit()
conn.close()
print("✅ Database tables created and sample data added!")