-- Create voters table
CREATE TABLE IF NOT EXISTS voters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    has_voted BOOLEAN DEFAULT FALSE
);

-- Create candidates table
CREATE TABLE IF NOT EXISTS candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    party VARCHAR(50) NOT NULL,
    image_url TEXT
);

-- Create votes table
CREATE TABLE IF NOT EXISTS votes (
    id SERIAL PRIMARY KEY,
    voter_id INTEGER REFERENCES voters(id),
    candidate_id INTEGER REFERENCES candidates(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample candidates
INSERT INTO candidates (name, party, image_url) VALUES
    ('kamala harris', 'Democratic', '/static/images/candidate1.jpg'),
    ('Donald Trump', 'Republican', '/static/images/candidate2.jpg')
ON CONFLICT DO NOTHING; 