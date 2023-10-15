CREATE TABLE IF NOT EXISTS Users (
    user_id INT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Urls (
    user_id INT,
    url VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS Favurls (
    user_id INT,
    url VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (url) REFERENCES Urls(url)
);

