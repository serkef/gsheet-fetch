-- CREATE TYPE record_category  AS ENUM ('case', 'death', 'recovery', 'severe', 'test', 'active');

CREATE TABLE IF NOT EXISTS record_changelog (
    id SERIAL,
    rec_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    rec_territory TEXT NOT NULL,
    rec_category record_category NOT NULL,
    rec_value INTEGER NOT NULL,
    CONSTRAINT unique_changelog_entry UNIQUE(rec_territory, rec_category, rec_value)
);

-- CREATE INDEX ON record_changelog (rec_ts DESC NULLS LAST, rec_territory, rec_category);
-- CREATE INDEX ON record_changelog (rec_ts DESC NULLS LAST);