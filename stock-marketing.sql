DESCRIBE master_stock_prices;

-- Check for missing values
SELECT 
    COUNT(*) AS total_rows,
    SUM(CASE WHEN Stock_Name IS NULL OR Stock_Name = '' THEN 1 ELSE 0 END) AS missing_names,
    SUM(CASE WHEN Date IS NULL THEN 1 ELSE 0 END) AS missing_dates,
    SUM(CASE WHEN Closing_Price IS NULL THEN 1 ELSE 0 END) AS missing_prices
FROM master_stock_prices;

-- Optional: Delete rows where critical values are NULL
DELETE FROM master_stock_prices 
WHERE Closing_Price IS NULL OR Date IS NULL;

-- Trend Analysis (Start to End Percentage Change)

WITH StockBounds AS (
    SELECT 
        Stock_Name,
        FIRST_VALUE(Closing_Price) OVER (
            PARTITION BY Stock_Name ORDER BY Date ASC
        ) AS Start_Price,
        FIRST_VALUE(Closing_Price) OVER (
            PARTITION BY Stock_Name ORDER BY Date DESC
        ) AS End_Price,
        FIRST_VALUE(Date) OVER (
            PARTITION BY Stock_Name ORDER BY Date ASC
        ) AS Start_Date,
        FIRST_VALUE(Date) OVER (
            PARTITION BY Stock_Name ORDER BY Date DESC
        ) AS End_Date,
        ROW_NUMBER() OVER (
            PARTITION BY Stock_Name ORDER BY Date DESC
        ) AS rn
    FROM master_stock_prices
)
SELECT 
    Stock_Name,
    Start_Date,
    Start_Price,
    End_Date,
    End_Price,
    ROUND(((End_Price - Start_Price) / Start_Price) * 100, 2) AS Percentage_Change,
    CASE 
        WHEN End_Price >= Start_Price THEN 'UP'
        ELSE 'DOWN'
    END AS Trend
FROM StockBounds
WHERE rn = 1
ORDER BY Percentage_Change DESC;

-- Buy and Sell Signals

SELECT 
    Stock_Name,
    Date,
    Closing_Price,
    ROUND(AVG(Closing_Price) OVER (
        PARTITION BY Stock_Name 
        ORDER BY Date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS Historical_Avg_Price,
    CASE 
        WHEN Closing_Price > AVG(Closing_Price) OVER (
            PARTITION BY Stock_Name 
            ORDER BY Date 
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) THEN 'BUY'
        ELSE 'SELL'
    END AS Signal_Recommendation
FROM master_stock_prices
ORDER BY Stock_Name, Date;

-- Maximum and Minimum Stock Price

SELECT 
    Stock_Name,
    MIN(Closing_Price) AS Min_Price,
    MAX(Closing_Price) AS Max_Price,
    ROUND(MAX(Closing_Price) - MIN(Closing_Price), 2) AS Price_Spread
FROM master_stock_prices
GROUP BY Stock_Name
ORDER BY Stock_Name;

-- Number of Buy / Sell Opportunities

SELECT 
    p.Stock_Name,
    COUNT(CASE WHEN p.Closing_Price = bounds.Min_Price THEN 1 END) AS Lowest_Buy_Opportunities,
    COUNT(CASE WHEN p.Closing_Price = bounds.Max_Price THEN 1 END) AS Highest_Sell_Opportunities
FROM master_stock_prices p
JOIN (
    SELECT 
        Stock_Name, 
        MIN(Closing_Price) AS Min_Price, 
        MAX(Closing_Price) AS Max_Price
    FROM master_stock_prices
    GROUP BY Stock_Name
) bounds ON p.Stock_Name = bounds.Stock_Name
GROUP BY p.Stock_Name
ORDER BY p.Stock_Name;

-- Percentage Change Analysis And Ranking

WITH StartEndPrices AS (
    SELECT 
        Stock_Name,
        FIRST_VALUE(Closing_Price) OVER (
            PARTITION BY Stock_Name ORDER BY Date ASC
        ) AS Start_Price,
        FIRST_VALUE(Closing_Price) OVER (
            PARTITION BY Stock_Name ORDER BY Date DESC
        ) AS End_Price,
        ROW_NUMBER() OVER (
            PARTITION BY Stock_Name ORDER BY Date DESC
        ) AS rn
    FROM master_stock_prices
)
SELECT 
    RANK() OVER (ORDER BY ((End_Price - Start_Price) / Start_Price) * 100 DESC) AS Performance_Rank,
    Stock_Name,
    Start_Price,
    End_Price,
    ROUND(((End_Price - Start_Price) / Start_Price) * 100, 2) AS Percentage_Change
FROM StartEndPrices
WHERE rn = 1;

-- Insights on Potential Profit

SELECT 
    Stock_Name,
    MIN(Closing_Price) AS Min_Buy_Price,
    MAX(Closing_Price) AS Max_Sell_Price,
    ROUND(MAX(Closing_Price) - MIN(Closing_Price), 2) AS Max_Profit_Per_Share,
    ROUND(((MAX(Closing_Price) - MIN(Closing_Price)) / MIN(Closing_Price)) * 100, 2) AS Max_Potential_Return_Pct
FROM master_stock_prices
GROUP BY Stock_Name
ORDER BY Max_Potential_Return_Pct DESC;