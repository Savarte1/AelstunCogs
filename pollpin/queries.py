POLLPIN_DB_INIT_1 = """
CREATE TABLE IF NOT EXISTS "pollpin_pins" (
    "id"	INTEGER,
    "poll_id"	INTEGER,
    "member"	INTEGER,
    "pin"	INTEGER,
    FOREIGN KEY("poll_id") REFERENCES "pollpin_polls"("id"),
    UNIQUE("poll_id","member"),
    UNIQUE("poll_id","pin")
);
"""
POLLPIN_DB_INIT_2 = """
CREATE TABLE IF NOT EXISTS "pollpin_polls" (
    "id"	INTEGER,
    "guild_id"	INTEGER,
    "name"	TEXT,
    "author"	INTEGER,
    "role"	INTEGER,
    PRIMARY KEY("id"),
    UNIQUE("guild_id","name")
);
"""
POLLPIN_MAKE_POLL = """
INSERT INTO pollpin_polls (guild_id, name, author, role)
VALUES (:guild, :name, :author, :role);
"""
POLLPIN_GET_POLLS = """
SELECT * FROM pollpin_polls WHERE guild_id = :guild;
"""
POLLPIN_GET_POLL = """
SELECT * FROM pollpin_polls WHERE guild_id = :guild AND name = :name;
"""


