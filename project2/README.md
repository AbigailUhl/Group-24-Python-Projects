# Automated Data Pipeline from Web APIs

 ## Group Members
- Abigail Uhl - ID: ATU22
- Larry Shi
- Nicolas Walker - ID: NW24e
- Harsh Thakor - ID: HJT24B

## Project Description
This project builds an automated data pipeline that collects daily weather data from a public API and stores it for future analysis. The pipeline retrieves weather data for multiple cities and saves it into a structured CSV file.

The real-world purpose of this project is to simulate how organizations track and store weather data over time for planning, forecasting, and analytics.

## API Used
Open-Meteo Weather API  
https://open-meteo.com/en/docs 

### Why this API?
We chose the Open-Meteo API because:
- It is free and requires no authentication  
- It provides structured JSON data  
- It allows multiple location queries

### Constraints
- No authentication required  
- Rate limits are minimal but still respected  
- Data is returned in JSON format  
- Requires multiple API calls for different cities  

## Data Pipeline Goals
- Fetch daily weather data for multiple cities (Tallahassee, Miami, Atlanta)  
- Extract key weather metrics (temperature, precipitation, wind speed, etc.)  
- Store results in a CSV file for long-term tracking  
- Append new data on each run instead of overwriting  
- Handle API errors gracefully without crashing  

## Project Structure
project-root/
│
├── README.md
├── src/
│ └── pipeline.py
├── data/
│ └── processed/
│ └── weather_data.csv

## How to Run the Pipeline
1. Ensure you are in project folder project2-automated-data-pipeline

2. python3 src/pipeline.py

## Example Run
Command:
```bash
python3 src/pipeline.py
```

Example Output:
```
Tallahassee: 200
Miami: 200
Atlanta: 200
Appended 21 rows to data/processed/weather_data.csv
```

## Columns
run_timestamp
city
date
temperature_max
temperature_min
precipitation_sum
wind_speed_max
