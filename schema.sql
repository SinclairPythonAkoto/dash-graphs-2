DROP TABLE if exists dash_graphs;
CREATE TABLE dash_graphs (
  id SERIAL PRIMARY KEY,
  name VARCHAR,
  first_visit VARCHAR,
  visit_again VARCHAR
  );