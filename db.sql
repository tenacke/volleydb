DROP DATABASE IF EXISTS VolleyDB;
CREATE DATABASE VolleyDB;
USE VolleyDB;

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
    password CHAR(200),
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

CREATE TABLE PlayerPositions (
    player_positions_id INT AUTO_INCREMENT,
    username CHAR(20),
    position INT, 
    PRIMARY KEY (player_positions_id),
    UNIQUE (username, position),
    FOREIGN KEY (username) REFERENCES Player(username),
	FOREIGN KEY (position) REFERENCES `Position`(position_id)
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
    contract_start DATE NOT NULL,
    contract_finish DATE NOT NULL,
    channel_id INT NOT NULL,
    PRIMARY KEY (team_id),
    FOREIGN KEY (coach_username) REFERENCES Coach(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES Channel(channel_id),
    CHECK (contract_start < contract_finish)
);

CREATE TABLE PlayerTeams (
    player_teams_id INT AUTO_INCREMENT,
    username CHAR(20),
    team INT,
    PRIMARY KEY (player_teams_id),
    UNIQUE (username, team),
    FOREIGN KEY (username) REFERENCES Player(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (team) REFERENCES Team(team_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE 
);

CREATE TABLE MatchSession (
    session_ID INT,
    time_slot INT,
    `date` DATE,
    rating FLOAT,
    team_id INT NOT NULL,
    stadium_id INT NOT NULL,
    assigned_jury_username CHAR(20) NOT NULL,
    PRIMARY KEY (session_ID),
    FOREIGN KEY (stadium_id) REFERENCES Stadium(stadium_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (assigned_jury_username) REFERENCES Jury(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CHECK (time_slot BETWEEN 1 AND 3)
);

CREATE TABLE SessionSquads (
    squad_id INT AUTO_INCREMENT,
    played_player_username CHAR(20) NOT NULL,
    session_ID INT NOT NULL,
    position_id INT NOT NULL,
    PRIMARY KEY (squad_id),
    UNIQUE (played_player_username, session_ID),
    FOREIGN KEY (played_player_username) REFERENCES Player(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (session_ID) REFERENCES MatchSession(session_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	FOREIGN KEY (position_id) REFERENCES `Position`(position_id)
);

INSERT INTO Position (position_id, position_name) VALUES ('0', 'Setter');
INSERT INTO Position (position_id, position_name) VALUES ('1', 'Outside Hitter');
INSERT INTO Position (position_id, position_name) VALUES ('2', 'Middle Blocker');
INSERT INTO Position (position_id, position_name) VALUES ('3', 'Opposite');
INSERT INTO Position (position_id, position_name) VALUES ('4', 'Libero');
INSERT INTO Stadium (stadium_id, stadium_name, stadium_country) VALUES ('0', 'Burhan Felek Voleybol Salonu', 'TR');
INSERT INTO Stadium (stadium_id, stadium_name, stadium_country) VALUES ('1', 'GD Voleybol Arena', 'TR');
INSERT INTO Stadium (stadium_id, stadium_name, stadium_country) VALUES ('2', 'Copper Box Arena', 'UK');
INSERT INTO Channel (channel_id, channel_name) VALUES ('0', 'BeIN Sports');
INSERT INTO Channel (channel_id, channel_name) VALUES ('1', 'Digiturk');
INSERT INTO Channel (channel_id, channel_name) VALUES ('2', 'TRT');
INSERT INTO User (username, password, name, surname) VALUES ('g_orge', 'Go.1993', 'Gizem ', 'Örge');
INSERT INTO User (username, password, name, surname) VALUES ('c_ozbay', 'Co.1996', 'Cansu ', 'Özbay');
INSERT INTO User (username, password, name, surname) VALUES ('m_vargas', 'Mv.1999', 'Melissa ', 'Vargas');
INSERT INTO User (username, password, name, surname) VALUES ('h_baladin', 'Hb.2007', 'Hande ', 'Baladın');
INSERT INTO User (username, password, name, surname) VALUES ('a_kalac', 'Ak.1995', 'Aslı ', 'Kalaç');
INSERT INTO User (username, password, name, surname) VALUES ('ee_dundar', 'Eed.2008', 'Eda Erdem ', 'Dündar');
INSERT INTO User (username, password, name, surname) VALUES ('z_gunes', 'Zg.2008', 'Zehra ', 'Güneş');
INSERT INTO User (username, password, name, surname) VALUES ('i_aydin', 'Ia.2007', 'İlkin ', 'Aydın');
INSERT INTO User (username, password, name, surname) VALUES ('e_sahin', 'Es.2001', 'Elif ', 'Şahin');
INSERT INTO User (username, password, name, surname) VALUES ('e_karakurt', 'Ek.2006', 'Ebrar ', 'Karakurt');
INSERT INTO User (username, password, name, surname) VALUES ('s_akoz', 'Sa.1991', 'Simge ', 'Aköz');
INSERT INTO User (username, password, name, surname) VALUES ('k_akman', 'Ka.2006', 'Kübra ', 'Akman');
INSERT INTO User (username, password, name, surname) VALUES ('d_cebecioglu', 'Dc.2007', 'Derya ', 'Cebecioğlu');
INSERT INTO User (username, password, name, surname) VALUES ('a_aykac', 'Aa.1996', 'Ayşe ', 'Aykaç');
INSERT INTO User (username, password, name, surname) VALUES ('user_2826', 'P.45825', 'Brenda', 'Schulz');
INSERT INTO User (username, password, name, surname) VALUES ('user_9501', 'P.99695', 'Erika', 'Foley');
INSERT INTO User (username, password, name, surname) VALUES ('user_3556', 'P.49595', 'Andrea', 'Campbell');
INSERT INTO User (username, password, name, surname) VALUES ('user_7934', 'P.24374', 'Beatrice', 'Bradley');
INSERT INTO User (username, password, name, surname) VALUES ('user_4163', 'P.31812', 'Betsey', 'Lenoir');
INSERT INTO User (username, password, name, surname) VALUES ('user_2835', 'P.51875', 'Martha', 'Lazo');
INSERT INTO User (username, password, name, surname) VALUES ('user_8142', 'P.58665', 'Wanda', 'Ramirez');
INSERT INTO User (username, password, name, surname) VALUES ('user_2092', 'P.16070', 'Eileen', 'Ryen');
INSERT INTO User (username, password, name, surname) VALUES ('user_3000', 'P.73005', 'Stephanie', 'White');
INSERT INTO User (username, password, name, surname) VALUES ('user_8323', 'P.33562', 'Daenerys', 'Targaryen');
INSERT INTO User (username, password, name, surname) VALUES ('d_santarelli', 'santa.really1', 'Daniele ', 'Santarelli');
INSERT INTO User (username, password, name, surname) VALUES ('g_guidetti', 'guidgio.90', 'Giovanni ', 'Guidetti');
INSERT INTO User (username, password, name, surname) VALUES ('f_akbas', 'a.fatih55', 'Ferhat ', 'Akbaş');
INSERT INTO User (username, password, name, surname) VALUES ('m_hebert', 'm.hebert45', 'Mike', 'Hebert');
INSERT INTO User (username, password, name, surname) VALUES ('o_deriviere', 'oliviere_147', 'Oliviere', 'Deriviere');
INSERT INTO User (username, password, name, surname) VALUES ('a_derune', 'aderune_147', 'Amicia', 'DeRune');
INSERT INTO User (username, password, name, surname) VALUES ('o_ozcelik', 'ozlem.0347', 'Özlem', 'Özçelik');
INSERT INTO User (username, password, name, surname) VALUES ('m_sevinc', 'mehmet.0457', 'Mehmet', 'Sevinç');
INSERT INTO User (username, password, name, surname) VALUES ('e_sener', 'ertem.4587', 'Ertem', 'Şener');
INSERT INTO User (username, password, name, surname) VALUES ('s_engin', 'sinan.6893', 'Sinan', 'Engin');
INSERT INTO User (username, password) VALUES ('Kevin', 'Kevin');
INSERT INTO User (username, password) VALUES ('Bob', 'Bob');
INSERT INTO User (username, password) VALUES ('sorunlubirarkadas', 'muvaffakiyetsizleştiricileştiriveremeyebileceklerimizdenmişsinizcesine');
INSERT INTO Jury (username, nationality) VALUES ('o_ozcelik', 'TR');
INSERT INTO Jury (username, nationality) VALUES ('m_sevinc', 'TR');
INSERT INTO Jury (username, nationality) VALUES ('e_sener', 'TR');
INSERT INTO Jury (username, nationality) VALUES ('s_engin', 'TR');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('g_orge', STR_TO_DATE('1993-04-26', '%Y-%m-%d'), '170', '59');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('c_ozbay', STR_TO_DATE('1996-10-17', '%Y-%m-%d'), '182', '78');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('m_vargas', STR_TO_DATE('1999-10-16', '%Y-%m-%d'), '194', '76');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('h_baladin', STR_TO_DATE('2007-09-01', '%Y-%m-%d'), '190', '81');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('a_kalac', STR_TO_DATE('1995-12-13', '%Y-%m-%d'), '185', '73');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('ee_dundar', STR_TO_DATE('2008-06-22', '%Y-%m-%d'), '188', '74');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('z_gunes', STR_TO_DATE('2008-07-07', '%Y-%m-%d'), '197', '88');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('i_aydin', STR_TO_DATE('2007-01-05', '%Y-%m-%d'), '183', '67');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('e_sahin', STR_TO_DATE('2001-01-19', '%Y-%m-%d'), '190', '68');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('e_karakurt', STR_TO_DATE('2006-01-17', '%Y-%m-%d'), '196', '73');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('s_akoz', STR_TO_DATE('1991-04-23', '%Y-%m-%d'), '168', '55');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('k_akman', STR_TO_DATE('2006-10-13', '%Y-%m-%d'), '200', '88');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('d_cebecioglu', STR_TO_DATE('2007-10-24', '%Y-%m-%d'), '187', '68');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('a_aykac', STR_TO_DATE('1996-02-27', '%Y-%m-%d'), '176', '57');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('user_2826', STR_TO_DATE('2002-12-13', '%Y-%m-%d'), '193', '80');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('user_9501', STR_TO_DATE('1995-12-21', '%Y-%m-%d'), '164', '62');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('user_3556', STR_TO_DATE('1996-04-26', '%Y-%m-%d'), '185', '100');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('user_7934', STR_TO_DATE('1997-05-28', '%Y-%m-%d'), '150', '57');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('user_4163', STR_TO_DATE('1993-05-07', '%Y-%m-%d'), '156', '48');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('user_2835', STR_TO_DATE('2001-05-20', '%Y-%m-%d'), '173', '71');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('user_8142', STR_TO_DATE('1994-01-03', '%Y-%m-%d'), '183', '94');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('user_2092', STR_TO_DATE('2004-06-21', '%Y-%m-%d'), '188', '60');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('user_3000', STR_TO_DATE('2002-05-19', '%Y-%m-%d'), '193', '74');
INSERT INTO Player (username, date_of_birth, height, weight) VALUES ('user_8323', STR_TO_DATE('2006-09-16', '%Y-%m-%d'), '222', '74');
INSERT INTO PlayerPositions (username, position) VALUES ('g_orge', '0');
INSERT INTO PlayerPositions (username, position) VALUES ('g_orge', '3');
INSERT INTO PlayerPositions (username, position) VALUES ('c_ozbay', '1');
INSERT INTO PlayerPositions (username, position) VALUES ('m_vargas', '2');
INSERT INTO PlayerPositions (username, position) VALUES ('h_baladin', '3');
INSERT INTO PlayerPositions (username, position) VALUES ('a_kalac', '4');
INSERT INTO PlayerPositions (username, position) VALUES ('ee_dundar', '4');
INSERT INTO PlayerPositions (username, position) VALUES ('z_gunes', '4');
INSERT INTO PlayerPositions (username, position) VALUES ('i_aydin', '1');
INSERT INTO PlayerPositions (username, position) VALUES ('i_aydin', '3');
INSERT INTO PlayerPositions (username, position) VALUES ('e_sahin', '1');
INSERT INTO PlayerPositions (username, position) VALUES ('e_sahin', '3');
INSERT INTO PlayerPositions (username, position) VALUES ('e_karakurt', '2');
INSERT INTO PlayerPositions (username, position) VALUES ('e_karakurt', '3');
INSERT INTO PlayerPositions (username, position) VALUES ('s_akoz', '0');
INSERT INTO PlayerPositions (username, position) VALUES ('k_akman', '0');
INSERT INTO PlayerPositions (username, position) VALUES ('k_akman', '4');
INSERT INTO PlayerPositions (username, position) VALUES ('d_cebecioglu', '3');
INSERT INTO PlayerPositions (username, position) VALUES ('d_cebecioglu', '4');
INSERT INTO PlayerPositions (username, position) VALUES ('a_aykac', '0');
INSERT INTO PlayerPositions (username, position) VALUES ('user_2826', '2');
INSERT INTO PlayerPositions (username, position) VALUES ('user_2826', '1');
INSERT INTO PlayerPositions (username, position) VALUES ('user_9501', '0');
INSERT INTO PlayerPositions (username, position) VALUES ('user_9501', '4');
INSERT INTO PlayerPositions (username, position) VALUES ('user_3556', '1');
INSERT INTO PlayerPositions (username, position) VALUES ('user_3556', '0');
INSERT INTO PlayerPositions (username, position) VALUES ('user_7934', '4');
INSERT INTO PlayerPositions (username, position) VALUES ('user_7934', '2');
INSERT INTO PlayerPositions (username, position) VALUES ('user_4163', '3');
INSERT INTO PlayerPositions (username, position) VALUES ('user_4163', '0');
INSERT INTO PlayerPositions (username, position) VALUES ('user_2835', '2');
INSERT INTO PlayerPositions (username, position) VALUES ('user_2835', '3');
INSERT INTO PlayerPositions (username, position) VALUES ('user_8142', '1');
INSERT INTO PlayerPositions (username, position) VALUES ('user_8142', '3');
INSERT INTO PlayerPositions (username, position) VALUES ('user_2092', '4');
INSERT INTO PlayerPositions (username, position) VALUES ('user_2092', '2');
INSERT INTO PlayerPositions (username, position) VALUES ('user_3000', '1');
INSERT INTO PlayerPositions (username, position) VALUES ('user_3000', '4');
INSERT INTO PlayerPositions (username, position) VALUES ('user_8323', '3');
INSERT INTO PlayerPositions (username, position) VALUES ('user_8323', '2');
INSERT INTO Coach (username, nationality) VALUES ('d_santarelli', 'ITA');
INSERT INTO Coach (username, nationality) VALUES ('g_guidetti', 'ITA');
INSERT INTO Coach (username, nationality) VALUES ('f_akbas', 'TUR');
INSERT INTO Coach (username, nationality) VALUES ('m_hebert', 'USA');
INSERT INTO Coach (username, nationality) VALUES ('o_deriviere', 'FRA');
INSERT INTO Coach (username, nationality) VALUES ('a_derune', 'FRA');
INSERT INTO Team (team_ID, team_name, coach_username, contract_start, contract_finish, channel_ID) VALUES ('0', 'Women A', 'd_santarelli', '2021-12-25', '2025-12-12', '0');
INSERT INTO Team (team_ID, team_name, coach_username, contract_start, contract_finish, channel_ID) VALUES ('1', 'Women B', 'g_guidetti', '2021-09-11', '2026-09-11', '1');
INSERT INTO Team (team_ID, team_name, coach_username, contract_start, contract_finish, channel_ID) VALUES ('2', 'U19', 'f_akbas', '2021-08-10', '2026-08-10', '0');
INSERT INTO Team (team_ID, team_name, coach_username, contract_start, contract_finish, channel_ID) VALUES ('3', 'Women B', 'f_akbas', '2000-08-10', '2015-08-10', '1');
INSERT INTO Team (team_ID, team_name, coach_username, contract_start, contract_finish, channel_ID) VALUES ('4', 'Women C', 'm_hebert', '2024-04-01', '2026-07-21', '1');
INSERT INTO Team (team_ID, team_name, coach_username, contract_start, contract_finish, channel_ID) VALUES ('5', 'U19', 'o_deriviere', '2015-08-10', '2020-08-09', '2');
INSERT INTO Team (team_ID, team_name, coach_username, contract_start, contract_finish, channel_ID) VALUES ('6', 'U19', 'a_derune', '2005-08-10', '2010-08-10', '2');
INSERT INTO PlayerTeams (username, team) VALUES ('g_orge', '0');
INSERT INTO PlayerTeams (username, team) VALUES ('g_orge', '1');
INSERT INTO PlayerTeams (username, team) VALUES ('c_ozbay', '1');
INSERT INTO PlayerTeams (username, team) VALUES ('m_vargas', '2');
INSERT INTO PlayerTeams (username, team) VALUES ('h_baladin', '3');
INSERT INTO PlayerTeams (username, team) VALUES ('a_kalac', '4');
INSERT INTO PlayerTeams (username, team) VALUES ('ee_dundar', '4');
INSERT INTO PlayerTeams (username, team) VALUES ('z_gunes', '4');
INSERT INTO PlayerTeams (username, team) VALUES ('i_aydin', '1');
INSERT INTO PlayerTeams (username, team) VALUES ('i_aydin', '3');
INSERT INTO PlayerTeams (username, team) VALUES ('e_sahin', '1');
INSERT INTO PlayerTeams (username, team) VALUES ('e_sahin', '3');
INSERT INTO PlayerTeams (username, team) VALUES ('e_karakurt', '2');
INSERT INTO PlayerTeams (username, team) VALUES ('e_karakurt', '3');
INSERT INTO PlayerTeams (username, team) VALUES ('s_akoz', '0');
INSERT INTO PlayerTeams (username, team) VALUES ('k_akman', '0');
INSERT INTO PlayerTeams (username, team) VALUES ('k_akman', '4');
INSERT INTO PlayerTeams (username, team) VALUES ('d_cebecioglu', '3');
INSERT INTO PlayerTeams (username, team) VALUES ('d_cebecioglu', '4');
INSERT INTO PlayerTeams (username, team) VALUES ('a_aykac', '0');
INSERT INTO PlayerTeams (username, team) VALUES ('user_2826', '2');
INSERT INTO PlayerTeams (username, team) VALUES ('user_2826', '1');
INSERT INTO PlayerTeams (username, team) VALUES ('user_9501', '0');
INSERT INTO PlayerTeams (username, team) VALUES ('user_9501', '4');
INSERT INTO PlayerTeams (username, team) VALUES ('user_3556', '1');
INSERT INTO PlayerTeams (username, team) VALUES ('user_3556', '0');
INSERT INTO PlayerTeams (username, team) VALUES ('user_7934', '4');
INSERT INTO PlayerTeams (username, team) VALUES ('user_7934', '2');
INSERT INTO PlayerTeams (username, team) VALUES ('user_4163', '3');
INSERT INTO PlayerTeams (username, team) VALUES ('user_4163', '0');
INSERT INTO PlayerTeams (username, team) VALUES ('user_2835', '2');
INSERT INTO PlayerTeams (username, team) VALUES ('user_2835', '3');
INSERT INTO PlayerTeams (username, team) VALUES ('user_8142', '1');
INSERT INTO PlayerTeams (username, team) VALUES ('user_8142', '3');
INSERT INTO PlayerTeams (username, team) VALUES ('user_2092', '4');
INSERT INTO PlayerTeams (username, team) VALUES ('user_2092', '2');
INSERT INTO PlayerTeams (username, team) VALUES ('user_3000', '1');
INSERT INTO PlayerTeams (username, team) VALUES ('user_3000', '4');
INSERT INTO PlayerTeams (username, team) VALUES ('user_8323', '3');
INSERT INTO PlayerTeams (username, team) VALUES ('user_8323', '2');
INSERT INTO MatchSession (session_ID, team_ID, stadium_ID, time_slot, `date`, assigned_jury_username, rating) VALUES ('0', '0', '0', '1', STR_TO_DATE('10.03.2024', '%d.%m.%Y'), 'o_ozcelik', '4.5');
INSERT INTO MatchSession (session_ID, team_ID, stadium_ID, time_slot, `date`, assigned_jury_username, rating) VALUES ('1', '1', '1', '1', STR_TO_DATE('03.04.2024', '%d.%m.%Y'), 'o_ozcelik', '4.9');
INSERT INTO MatchSession (session_ID, team_ID, stadium_ID, time_slot, `date`, assigned_jury_username, rating) VALUES ('2', '0', '1', '3', STR_TO_DATE('03.04.2024', '%d.%m.%Y'), 'o_ozcelik', '4.4');
INSERT INTO MatchSession (session_ID, team_ID, stadium_ID, time_slot, `date`, assigned_jury_username, rating) VALUES ('3', '2', '2', '2', STR_TO_DATE('03.04.2024', '%d.%m.%Y'), 'm_sevinc', '4.9');
INSERT INTO MatchSession (session_ID, team_ID, stadium_ID, time_slot, `date`, assigned_jury_username, rating) VALUES ('4', '3', '2', '2', STR_TO_DATE('03.04.2023', '%d.%m.%Y'), 'e_sener', '4.5');
INSERT INTO MatchSession (session_ID, team_ID, stadium_ID, time_slot, `date`, assigned_jury_username, rating) VALUES ('5', '3', '1', '1', STR_TO_DATE('27.05.2023', '%d.%m.%Y'), 's_engin', '4.4');
INSERT INTO MatchSession (session_ID, team_ID, stadium_ID, time_slot, `date`, assigned_jury_username, rating) VALUES ('6', '0', '1', '1', STR_TO_DATE('01.09.2022', '%d.%m.%Y'), 'm_sevinc', '4.6');
INSERT INTO MatchSession (session_ID, team_ID, stadium_ID, time_slot, `date`, assigned_jury_username, rating) VALUES ('7', '0', '2', '3', STR_TO_DATE('02.05.2023', '%d.%m.%Y'), 'o_ozcelik', '4.7');
INSERT INTO MatchSession (session_ID, team_ID, stadium_ID, time_slot, `date`, assigned_jury_username, rating) VALUES ('8', '1', '0', '1', STR_TO_DATE('10.03.2024', '%d.%m.%Y'), 'o_ozcelik', '4.5');
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('0', 'g_orge', 0);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('0', 'c_ozbay', 1);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('0', 'm_vargas', 2);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('0', 'h_baladin', 3);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('0', 'a_kalac', 4);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('0', 'ee_dundar', 4);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('1', 'c_ozbay', 1);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('1', 'm_vargas', 2);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('1', 'i_aydin', 1);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('1', 'a_kalac', 4);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('1', 's_akoz', 0);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('1', 'd_cebecioglu', 3);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('2', 'g_orge', 3);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('2', 'm_vargas', 2);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('2', 'c_ozbay', 1);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('2', 'a_kalac', 4);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('2', 's_akoz', 0);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('2', 'a_aykac', 0);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('3', 'ee_dundar', 4);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('3', 'h_baladin', 3);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('3', 'z_gunes', 4);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('3', 'i_aydin', 3);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('3', 'e_karakurt', 2);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('3', 'k_akman', 0);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('4', 'user_2826', 2);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('4', 'user_9501', 0);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('4', 'user_3556', 1);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('4', 'user_7934', 4);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('4', 'user_4163', 3);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('4', 'user_2835', 2);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('5', 'user_2826', 1);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('5', 'user_9501', 4);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('5', 'user_3556', 0);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('5', 'user_7934', 2);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('5', 'user_4163', 0);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('5', 'user_2835', 3);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('6', 'g_orge', 0);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('6', 'm_vargas', 2);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('6', 'c_ozbay', 1);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('6', 'a_kalac', 4);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('6', 'e_karakurt', 3);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('6', 'a_aykac', 0);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('7', 'g_orge', 3);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('7', 'm_vargas', 2);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('7', 'c_ozbay', 1);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('7', 'a_kalac', 4);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('7', 'e_karakurt', 2);
INSERT INTO SessionSquads (session_ID, played_player_username, position_id) VALUES ('7', 'a_aykac', 0);

DELIMITER $$
CREATE TRIGGER check_time_slot BEFORE INSERT ON MatchSession
FOR EACH ROW
BEGIN
    IF NEW.time_slot = 1 THEN
        IF EXISTS (SELECT stadium_id, `date`, time_slot FROM MatchSession WHERE stadium_id = NEW.stadium_id AND `date` = NEW.`date` AND time_slot < 3) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Time slot is already taken for this stadium and date';
        END IF;
    END IF;
    IF NEW.time_slot = 2 THEN
        IF EXISTS (SELECT stadium_id, `date`, time_slot FROM MatchSession WHERE stadium_id = NEW.stadium_id AND `date` = NEW.`date`) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Time slot is already taken for this stadium and date';
        END IF;
    END IF;
    IF NEW.time_slot = 3 THEN
        IF EXISTS (SELECT stadium_id, `date`, time_slot FROM MatchSession WHERE stadium_id = NEW.stadium_id AND `date` = NEW.`date` AND time_slot > 1) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Time slot is already taken for this stadium and date';
        END IF;
    END IF;
END; $$

CREATE TRIGGER check_position BEFORE INSERT ON SessionSquads
FOR EACH ROW
BEGIN
	DECLARE potential_error_message VARCHAR(100);
    SET potential_error_message = CONCAT('Player ', NEW.played_player_username, ' does not play in this position');

    IF NOT EXISTS (SELECT * FROM PlayerPositions WHERE username = NEW.played_player_username AND position = NEW.position_id) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = potential_error_message;
    END IF;
END; $$
DELIMITER ;