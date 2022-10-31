INIT_POLLPIN_DB = """
CREATE TABLE IF NOT EXISTS "pollpin_polls" (
    "id" INTEGER,
    "guild" INTEGER,
    "poll" TEXT,
    "owner" INTEGER,
    "role" INTEGER,
    UNIQUE("guild","poll"),
    PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "pollpin_pins" (
    "id" INTEGER,
    "poll_id" INTEGER,
    "user" INTEGER,
    "pin" INTEGER,
    UNIQUE("poll_id","pin"),
    UNIQUE("poll_id","user"),
    PRIMARY KEY("id"),
    FOREIGN KEY("poll_id") REFERENCES "pollpin_polls"
);
"""

SELECT_PIN = """
SELECT 
"""