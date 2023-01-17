POLLPIN_DB = """
CREATE TABLE IF NOT EXISTS "pollpin_pins" (
	"id"	INTEGER,
	"poll_id"	INTEGER,
	"member"	INTEGER,
	"pin"	INTEGER,
	FOREIGN KEY("poll_id") REFERENCES "pollpin_polls"("id"),
	UNIQUE("poll_id","member"),
	UNIQUE("poll_id","pin")
);
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

