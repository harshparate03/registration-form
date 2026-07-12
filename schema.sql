CREATE TABLE IF NOT EXISTS registrations (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    date_value DATE,
    time_value TIME,
    mobile VARCHAR(20) NOT NULL,
    website TEXT,
    gender VARCHAR(20) NOT NULL,
    skills TEXT,
    city VARCHAR(100) NOT NULL,
    image_name TEXT NOT NULL,
    image_mime VARCHAR(100) NOT NULL,
    image_data BYTEA NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);