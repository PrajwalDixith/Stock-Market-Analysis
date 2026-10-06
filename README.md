Stock Market Analysis with SQL 

Objective: 
Analyze stock performance using historical stock data, generate insights using SQL, and create 
a detailed report on stock trends, buy/sell recommendations, and percentage changes. 

This project include to answer all fallowing tasks with simple video explanation with conclusions.

Part 1: Data Loading and Setup 
Task: 
You are given multiple datasets representing stock prices for different companies: 
● Eicher Motors 
● Bajaj Auto 
● TCS 
● TVS Motors 
● Hero Motocorp 
● Infosys 
Each dataset contains stock prices for each company over time. Your first task is to load these 
datasets into a database system (like MySQL, PostgreSQL, or SQLite). 

Part 2: Data Preprocessing 
Task: 
1. Load all CSV files into separate tables in the SQL database. 
2. Clean the data (handle missing values, incorrect data types, etc.). 
3. Ensure the dataset has the following structure: 
○ Stock Name: The name of the company (e.g., Infosys, TCS). 
○ Date: Date of stock price. 
○ Closing Price: The closing stock price for that day. 

Part 3: SQL Queries 
You need to perform the following analysis using SQL queries: 
1. Trend Analysis: 
   ○ Identify whether the stock price is trending up or down based on the data from 
the earliest and latest dates. Write a query to calculate the percentage change in 
stock price between the start and end date. 
   ○ Example query: Calculate the percentage change in stock price for Eicher 
Motors from 01-01-2015 to 31-07-2018. 

2. Buy and Sell Signals: 
   ○ Identify potential buy and sell signals. Create SQL queries that check for stock 
price increases or decreases based on specific criteria. For example: 
   ■ If the stock price shows an increasing trend for several consecutive days, 
this might be a signal to "buy". 
   ■ If the stock price shows a consistent decrease, it might be a signal to 
"sell". 
   ○ Create a table with recommendations on whether to "buy" or "sell" each stock. 

3. Maximum and Minimum Stock Price: 
   ○ Find the highest and lowest closing stock price for each company during the 
entire period. Write SQL queries to find these values. 

4. Number of Buy/Sell Opportunities: 
   ○ Calculate how many times you could have bought and sold each stock for the 
highest profit based on the data. A possible strategy could be to buy at the lowest 
point and sell at the highest point during the available dates. 

5. Percentage Change Analysis: 
  ○ Calculate the percentage change in stock value from the start date to the end 
date for each stock and rank the stocks based on the percentage increase or 
decrease. 
   ○ Example: Compare stock values of Bajaj Auto from 01-01-2015 to 31-07
2018 and find the percentage change. 

Part 4: Report and Insights 
Task: 
Based on your SQL queries and analysis, create a detailed report summarizing the following: 

1. Stock Trends: 
Provide a brief overview of the trend (up/down) for each company, based on the 
percentage change analysis. 

2. Buy/Sell Recommendations: 
   ○ Include a list of recommendations on which stocks to buy or sell based on 
historical trends. 
   ○ For example, "Bajaj Auto has an increasing trend and should be bought, while 
TCS has a decreasing trend and should be sold." 

3. Insights on Potential Profit: 
Calculate the potential profit from buying and selling the stocks at optimal times based 
on your SQL analysis.
