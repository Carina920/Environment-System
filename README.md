## Setup

- install `mysqlclient` python library
    - run `pip install mysqlclient`
- if not existed, create a database(schema) called `cs411pt1`, otherwise, drop existed database then create this one
- modify `cs411pt1/settings.py` file
    - change settings in `DATABASES` section to appropriate values
- in terminal, navigate to the root folder of this project, 
    - run `python manage.py makemigrations`
    - run `python manage.py migrate`
    - run `python manage.py createsuperuser`
        -  note: this step will create a superuser account with which we can use it to log into admin site to check our database without using Mysql Workbench
- to populate the database
    - run `python manage.py populate_database`
- create Trigger and Stored Procedure
	- executing the sql displayed in later section to set up trigger and stored procedure 

## Trigger

correct invalid timezone input value.
```
delimiter //
CREATE TRIGGER valid_timezone BEFORE UPDATE ON cs411pt1.userprofile FOR EACH ROW
BEGIN
	IF NEW.TimeZone > 14 THEN
		SET NEW.TimeZone = 0;
	ELSEIF  NEW.TimeZone < -12 THEN
		SET NEW.TimeZone = 0;
	END IF;
END; //
delimiter ;
```

## Stored Procedure

Following stored procedure will return the most searched weather type and location and searched times in this month, it will also return number of user that searched same weather type or location as that of current user, besides, it will return one of those users as a friend recommendation to current user.
```
delimiter //
CREATE PROCEDURE hotevent (IN user_id INT)
BEGIN    
    DECLARE hotSearchedWeather VARCHAR(32);
    DECLARE hotSearchedWeatherSearchedTimes INT;
	DECLARE hotSearchedState VARCHAR(16);
    DECLARE hotSearchedCity VARCHAR(32);
    DECLARE hotSearchedLocationSearchedTimes INT;
    
	DROP TABLE IF EXISTS similaruser;
	CREATE TABLE similaruser (
		UserId INT PRIMARY KEY
	);
    
    DROP TABLE IF EXISTS hoteventtable;
    -- Find all events that are searched by any user in past month, store is in table to be reused later
    CREATE TABLE hoteventtable 
    SELECT LocationId, WeatherTypeId, UserId
	FROM cs411pt1.usersearchhistory AS s LEFT JOIN cs411pt1.event AS e ON (s.EventId = e.id)
	WHERE YEAR(SearchedDate) = YEAR(CURRENT_DATE()) AND MONTH(SearchedDate) = MONTH(CURRENT_DATE());
    
    -- Find the most searched weather type among all user in past month
    SELECT TypeName, COUNT(*) AS searchedTimes INTO hotSearchedWeather, hotSearchedWeatherSearchedTimes
	FROM hoteventtable AS h LEFT JOIN cs411pt1.weathertype AS e ON (h.WeatherTypeId = e.id)
	GROUP BY WeatherTypeId
	HAVING searchedTimes > 0
	ORDER BY searchedTimes DESC
	LIMIT 1;   

	-- Find the most searched location among all user in past month
	SELECT State, City, COUNT(*) AS searchedTimes INTO hotSearchedState, hotSearchedCity, hotSearchedLocationSearchedTimes
	FROM hoteventtable AS h LEFT JOIN cs411pt1.location AS e ON (h.LocationId = e.id)
	GROUP BY LocationId
	HAVING searchedTimes > 0
	ORDER BY searchedTimes DESC
	LIMIT 1;
    
    -- Creative function, friend recommendation: 
    -- Find the one user that have search same weather type or location as that of current user in past month  
    BEGIN		
		DECLARE done BOOLEAN DEFAULT FALSE;
		DECLARE cur CURSOR FOR (SELECT LocationId, WeatherTypeId, UserId FROM hoteventtable WHERE UserId != user_id);
		DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
        
        -- Find searched weather by current use
        SET @userSearchedWeatherId = (SELECT GROUP_CONCAT(DISTINCT(WeatherTypeId)) FROM hoteventtable WHERE UserId = user_id);        
        -- Find most searched location by current use
		SET @userSearchedLocationId = (SELECT GROUP_CONCAT(DISTINCT(LocationId)) FROM hoteventtable WHERE UserId = user_id); 
        
        -- Find all user that has similar search history
		OPEN cur;
		BEGIN 
			DECLARE w_id INT;
            DECLARE l_id INT;
            DECLARE u_id INT;
			
			REPEAT
				FETCH cur INTO l_id, w_id, u_id;
				
				IF FIND_IN_SET(l_id, @userSearchedLocationId) > 0 THEN
					INSERT IGNORE INTO similaruser VALUES(u_id);
				ELSEIF FIND_IN_SET(w_id, @userSearchedWeatherId) > 0 THEN
					INSERT IGNORE INTO similaruser VALUES(u_id);
				END IF;
			UNTIL done
			END REPEAT;
		END;
		CLOSE cur;
    END;
    
    -- Find the number of user that have similar search history as that of current user
    SET @numOfUserHasSimilarSearchHistory = (SELECT COUNT(*) FROM similaruser);
    -- Randomly select one user to recommend to current user
    SET	@userWithSimilarSearchHistory = (SELECT Name 
										 FROM cs411pt1.userprofile 
										 WHERE UserId = (SELECT UserId FROM similaruser ORDER BY RAND() LIMIT 1)
                                         LIMIT 1);
    
    DROP TABLE IF EXISTS similaruser;
    DROP TABLE IF EXISTS hoteventtable;
    
	SELECT hotSearchedWeather, hotSearchedWeatherSearchedTimes, hotSearchedState, hotSearchedCity, hotSearchedLocationSearchedTimes, @numOfUserHasSimilarSearchHistory, @userWithSimilarSearchHistory;
END//
delimiter ;
```
