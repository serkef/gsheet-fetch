INSERT INTO
    record_changelog (rec_territory, rec_category, rec_value)
VALUES
    (%s, %s, %s)
ON CONFLICT ON CONSTRAINT unique_changelog_entry DO NOTHING
