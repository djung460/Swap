CREATE TABLE Student(
    username VARCHAR(32) NOT NULL,
    pwhash BINARY(60) NOT NULL,
    year INT NOT NULL,
    faculty CHAR(4) NOT NULL,
    email VARCHAR(64) NOT NULL,
    name VARCHAR(128) NOT NULL,
    phoneNumber CHAR(12) NOT NULL,

    PRIMARY KEY (username)
);
CREATE TABLE Instructor(
    username VARCHAR(32) NOT NULL,
    pwhash BINARY(60) NOT NULL,
    faculty CHAR(4) NOT NULL,
    email VARCHAR(64) NOT NULL,
    name VARCHAR(128) NOT NULL,
    phoneNumber CHAR(12) NOT NULL,

    PRIMARY KEY (username)
);
CREATE TABLE Equipment(
    equipmentID INT NOT NULL,
    equipmentName VARCHAR(128) NOT NULL,
    equipmentType CHAR(3) NOT NULL,

    PRIMARY KEY (equipmentID)
);

CREATE TABLE Class(
    faculty CHAR(4) NOT NULL,
    classNum CHAR(4) NOT NULL,
    term CHAR(7) NOT NULL,
    instructorUsername VARCHAR(32) NOT NULL,

    PRIMARY KEY(faculty, classNum, term),
    FOREIGN KEY(instructorUsername)
        REFERENCES Instructor(username)
        ON DELETE CASCADE
);
CREATE TABLE ClassRequiresEquipment(
    faculty CHAR(4) NOT NULL,
    classNum CHAR(4) NOT NULL,
    term CHAR(7) NOT NULL,
    equipmentID INT NOT NULL

    PRIMARY KEY (faculty, classNum, term, equipmentID),
    FOREIGN KEY(faculty, classNum, term)
        REFERENCES Class (faculty, classNum, term)
        ON DELETE CASCADE,
    FOREIGN KEY(equipmentID)
        REFERENCES Equipment(equipmentID)
);
CREATE TABLE StudentHasEquipment(
    username VARCHAR(32) NOT NULL,
    equipmentID INT NOT NULL,
    quantity INT NOT NULL, 

    PRIMARY KEY (username, equipmentID),
    FOREIGN KEY(username)
        REFERENCES Student(username)
        ON DELETE CASCADE,
    FOREIGN KEY(equipmentID)
        REFERENCES Equipment(equipmentID)
);
CREATE TABLE StudentTakesClass(
    username VARCHAR(32) NOT NULL,
    faculty CHAR(4) NOT NULL,
    classNum CHAR(4) NOT NULL,
    term CHAR(7) NOT NULL,

    PRIMARY KEY (username,faculty, classNum, term),
    FOREIGN KEY(faculty, classNum, term)
        REFERENCES Class(faculty, classNum, term)
        ON DELETE CASCADE,
    FOREIGN KEY(username)
        REFERENCES Student(username)
        ON DELETE CASCADE
);
CREATE TABLE PendingTrade(
    tradeID INTEGER PRIMARY KEY AUTOINCREMENT,
    requestUsername VARCHAR(32) NOT NULL,
    responseUsername VARCHAR(32) NOT NULL,
    requestEquipID INT NOT NULL,
    responseEquipID INT NOT NULL,
    requestConfirm INT NOT NULL,
    responseConfirm INT NOT NULL,
    dateRequested DATETIME NOT NULL,

    FOREIGN KEY(requestUsername, requestEquipID)
        REFERENCES StudentHasEquipment(username, equipmentID),
    FOREIGN KEY(responseUsername, responseEquipID)
        REFERENCES StudentHasEquipment(username, equipmentID)
);
CREATE TABLE ConfirmedTrade(
    tradeID INTEGER PRIMARY KEY AUTOINCREMENT,
    requestUsername VARCHAR(32) NOT NULL,
    responseUsername VARCHAR(32) NOT NULL,
    requestEquipID INT NOT NULL,
    responseEquipID INT NOT NULL,
    dateConfirmed DATETIME NOT NULL,

    FOREIGN KEY(requestUsername)
        REFERENCES Student(username),
    FOREIGN KEY(requestEquipID)
        REFERENCES Equipment(equipmentID),
    FOREIGN KEY(responseUsername)
        REFERENCES Student(username),
    FOREIGN KEY(responseEquipID)
        REFERENCES Equipment(equipmentID)
);

