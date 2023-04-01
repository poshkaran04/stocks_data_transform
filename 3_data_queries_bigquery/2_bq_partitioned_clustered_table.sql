CREATE OR REPLACE TABLE `data-bootcamp-380922.us_stocks.stocks_data_usa_partitioned`
(
  Stock_Symbol STRING,
  Date DATE,
  Open FLOAT64,
  High FLOAT64,
  Low FLOAT64,
  Close FLOAT64,
  Volume INTEGER,
  Last_Import_Date TIMESTAMP
)
PARTITION BY Date 
CLUSTER BY Stock_Symbol
AS
SELECT 

  REPLACE(Filename, '.us.txt', '') as Stock_Symbol 
, Date
, Open
, High
, Low
, Close
, Volume
, CURRENT_TIMESTAMP() AS Last_Import_Date,

FROM `data-bootcamp-380922.us_stocks.stocks_data_usa` 
WHERE Date>='2007-01-01'