# Environment-System
Database Centric Web Application with Django

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

