# Environment-System
Coursework project at UIUC (CS 411): collaborated with other two teammates on developing the Database Centric Web Application with Django.

PS: The coding part is in the 'Coding' branch.

## Introduction
### Project Summary
This is a project about collecting and displaying natural environment-related information. It aims to provide users with an easier way with just a few clicks to obtain local environmental information in specific places. It can be applied for personal searching, weather bureau, and government. It is a web-driven and data-memorable system.

### Project Overview
Our project aims to build a system that displays information on wind, rainfall, sunlight, CO2, topography, and other natural environmental data of countries from all over the world. It can be divided into three parts: data collection, website, and customization.

For data collection, all the data will be manually downloaded from NASA, NOAA, and Kaggle, then we will use python scripts to preprocess all the data and import them into the database using the python-SQL library. The database may be updated and manipulated when the user interacts with the website. Some basic attributes include city, state, or county and time range covering past, current, or future.

The website will provide functions of searching based on location and time. Also, users will have the ability to create their own accounts and user profile. The program will use user profiles to display recommendations. 

For customization, we will support the user profiles. Each user can have their personal account and the project will generate recommendations based on user profile and frequently searched keywords. The data displayed on the website cannot be directly manipulated by users, except their personal profiles.

### Data Collection
For our project, we used the following datasets: [kaggle](https://www.kaggle.com/threnjen/40-years-of-air-quality-index-from-the-epa-daily). That dataset contains too much weather event records, to reduce the size of our database, we only select the events that happens within 2 years and in the US.

## Technology
*Languages:* Javascript, HTML, CSS, Python

*Framework:* Django

*Database:* MySQL

## Application
For our application, we used a MySQL/GCP and Django to build a full-stack web application. 

For visitors:
1. Register an account.

For registered users:
1. Log in and customize personal profile.
2. Search the natural environmental information by weather types, locations and more.
3. See the most populate searching history.
4. See the recommended information based on their profiles.

### Basic Functions of Web Application
Search. Users will have the ability to search environmental data based on location and time.

Log in. Users will have the ability to create their own accounts and user profile. 

### Creative Component
Friend Recommendation. The system will recommend current user to another user that have similar search history. The similarity is determined by if the most popular weather event type or location searched by two users are the same, if so, the system will recommend them to each other.

### Advanced Database Program
For this project we decided to use a stored procedure and trigger approach. 

We decided to implement a stored procedure to help our recommendation engine as well as search trend by all users. Our stored procedure parses the history of user searches, calculates the weather types they search most often, the locations they search most often, and so on. In addition, the stored procedure then stores this data in the user preference table. Our front end can provide users with the most searched weather types of the month, the most searched locations of the month, and so on. Stored procedures allow us to calculate important information in the database itself.

### Dataflow
When user visits our website, it requires a login to continue.

![image](https://user-images.githubusercontent.com/59858652/149225075-0a77e478-67ae-4de9-b092-0b6c34f1310c.png)

After user log in, the home page will display, which include the most recent weather event.

![image](https://user-images.githubusercontent.com/59858652/149225115-4512ea14-b991-454c-af09-5d53a7db7e0a.png)

In the home page, user can search the weather event by selecting options from the dropdown or by type key words in "Vague Search" section.

![image](https://user-images.githubusercontent.com/59858652/149225150-0654af22-1230-431c-859b-749425c46a1a.png)

In the search history page, user can delete any of the history by id. User can also see the search trend from the this month as well as the friend recommendation result.

![image](https://user-images.githubusercontent.com/59858652/149225184-5b1c707d-9039-4905-98ce-abd2ebbee3e4.png)

In Profile page, user can customize their info and overview section will display the weather summary based on user's location.

![image](https://user-images.githubusercontent.com/59858652/149225200-4ffa2f6f-201f-4d77-a927-28b2156572fc.png)

## Teamwork
My responsibility was to take charge of front-end design, basic function design, indexing for advanced SQL, and the design of the recommendation system.
