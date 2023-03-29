with
    stocks_data as (select * from {{ ref("stg_stocks_data_us") }})

    ,stocks_name as (select * from {{ ref("stg_stocks_names_us") }})
select

    stock_symbol,
    name as stock_name,
    sector as stock_sector,
    industry as stock_industry,
    date,
    open,
    high,
    low,
    close,
    volume

from stocks_data d
join stocks_name n on d.stock_symbol = n.symbol
