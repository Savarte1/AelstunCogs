INIT_NSCONNECT_DB = """
CREATE TABLE IF NOT EXISTS "nsv_nations" (
    "id" INTEGER,
    "dbid" INTEGER UNIQUE,
    "nation" TEXT,
    "region" TEXT,
    "wa_member" INTEGER,
    "exists" INTEGER,
    PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "nsv_users" (
    "id" INTEGER,
    "user" INTEGER,
    "nation_id" INTEGER,
    FOREIGN KEY("nation_id") REFERENCES "nsv_nations"("id"),
    PRIMARY KEY("id")
);
"""