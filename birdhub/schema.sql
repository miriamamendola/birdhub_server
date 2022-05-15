DROP TABLE IF EXISTS photo;

CREATE TABLE photo (
  photo_id INTEGER PRIMARY KEY AUTOINCREMENT,
  photo_ts TIMESTAMP UNIQUE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  photo_name TEXT UNIQUE NOT NULL
);
/* filename =bird+id */

INSERT INTO photo (photo_name) VALUES ('/images/bird000.jpg');  