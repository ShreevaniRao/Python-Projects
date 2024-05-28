/* queries to analyse the loaded data from the pandas dataframe to obtain useful insights */

--find top 10 highest revenue generating products 

select top 10 product_id, sum(sale_price * quantity) as revenue
from df_orders
group by product_id
order by revenue desc

--find top 5 highest selling products in each region

with highest_selling_products as (
select product_id, region 
, sum(sale_price * quantity) as revenue
,ROW_NUMBER() over (partition by region order by sum(sale_price * quantity)  desc) as rn
from df_orders
group by region, product_id
)
select rn,region,product_id,revenue
from  highest_selling_products pr
where rn <=5 

--find month over month growth comparison for 2022 and 2023 sales eg : jan 2022 vs jan 2023

with year_and_month_sales as (
select year(order_date) as order_year
,month(order_date) as order_month
,sum(sale_price) as sales
from df_orders
group by year(order_date),month(order_date)
)
select  DateName( month , DateAdd( month , order_month , 0 ) - 1 ) as 'month'
, sum(case when order_year=2022 then sales else 0 end) as sales_2022
, sum(case when order_year=2023 then sales else 0 end) as sales_2023
from year_and_month_sales 
group by order_month
order by order_month

--for each category which month had highest sales 

with highest_selling_products_category_month as (
select 
category
,MONTH(order_date) as month_number
,sum(sale_price * quantity) as revenue
,ROW_NUMBER() over (partition by category order by sum(sale_price * quantity)  desc) as rn
from df_orders
group by category,month(order_date) 
)
select category,DateName( month , DateAdd( month , month_number , 0 ) - 1 ) as 'month', revenue
from  highest_selling_products_category_month pr
where rn = 1 

--which sub category had highest growth by profit in 2023 compare to 2022


with year_and_sub_category_sales as (
select year(order_date) as order_year
,sub_category 
,sum(profit )  as profit
from df_orders
group by year(order_date),sub_category
)
, sub_category_growth as (
select sub_category
, sum(case when order_year=2022 then profit else 0 end) as sales_2022
, sum(case when order_year=2023 then profit else 0 end) as sales_2023
from year_and_sub_category_sales 
group by sub_category)

select top 1 sub_category
,sales_2023,sales_2022
,(sales_2023-sales_2022) as growth
from  sub_category_growth
order by (sales_2023-sales_2022) desc