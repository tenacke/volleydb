CREATE TABLE Position (
    position_id INT,
    position_name CHAR(20),
    PRIMARY KEY (position_id)
);

CREATE TABLE Stadium (
    stadium_id INT,
    stadium_name CHAR(50),
    stadium_country CHAR(20),
    PRIMARY KEY (stadium_id)
);

CREATE TABLE User (
    username CHAR(20),
    password CHAR(20),
    name CHAR(20),
    surname CHAR(20),
    PRIMARY KEY (username)
);

CREATE TABLE Player (
    username CHAR(20),
    date_of_birth DATE,
    height FLOAT,
    weight FLOAT,
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES User(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE PlaysInPosition (
    username CHAR(20),
    position_id INT, 
    PRIMARY KEY (username, position_id),
    FOREIGN KEY (username) REFERENCES Player(username),
	FOREIGN KEY (position_id) REFERENCES `Position`(position_id)
);

CREATE TABLE Coach (
    username CHAR(20),
    nationality CHAR(20) NOT NULL,
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES User(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Jury (
    username CHAR(20),
    nationality CHAR(20) NOT NULL,
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES User(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Channel (
    channel_id INT,
    channel_name CHAR(20),
    PRIMARY KEY (channel_id)
);

CREATE TABLE Team (
    team_id INT,
    team_name CHAR(20),
    coach_username CHAR(20) NOT NULL,
    coach_contract_start DATE NOT NULL,
    coach_contract_end DATE NOT NULL,
    channel_id INT NOT NULL,
    PRIMARY KEY (team_id),
    FOREIGN KEY (coach_username) REFERENCES Coach(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES Channel(channel_id),
    CHECK (coach_contract_start < coach_contract_end)
);

CREATE TABLE PlaysForTeam (
    username CHAR(20),
    team_id INT,
    PRIMARY KEY (username, team_id),
    FOREIGN KEY (username) REFERENCES Player(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE 
);

CREATE TABLE MatchSession (
    match_id INT,
    time_slot INT,
    match_date DATE,
    rating FLOAT,
    team_id INT NOT NULL,
    stadium_id INT NOT NULL,
    jury_username CHAR(20) NOT NULL,
    PRIMARY KEY (match_id),
    UNIQUE (match_id, jury_username),
    UNIQUE (match_date, time_slot, stadium_id),
    FOREIGN KEY (stadium_id) REFERENCES Stadium(stadium_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (jury_username) REFERENCES Jury(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CHECK (time_slot BETWEEN 1 AND 3)
);

CREATE TABLE PlaysInSession (
    username CHAR(20) NOT NULL,
    match_id INT NOT NULL,
    position_id INT NOT NULL,
    PRIMARY KEY (username, match_id),
    FOREIGN KEY (username) REFERENCES Player(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (match_id) REFERENCES MatchSession(match_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	FOREIGN KEY (position_id) REFERENCES `Position`(position_id)
);

