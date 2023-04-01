# US Stock Market Analysis
<b>Problem description</b>
The objective of this project is to analyze complex USA stocks data from 2011 in order to provide an average investor with a better understanding of the stock market. The data is distributed by individual stock names and sectors to provide users with a comprehensive view of the market. The final output is a Power BI dashboard, consisting of two charts: a line chart showing day-to-day stock performance and a bar chart showing the top 5 sectors in the USA market. By analyzing the data in this way, the project aims to provide users with valuable insights that can help inform their investment decisions.

<b>Tools and Technologies used</b>
1. Terraform - Used to automate the deployment and management of infrastructure on Google Cloud Platform (GCP), including BigQuery and Google Cloud Storage.

<i>Instructions</i>
Terraform is a tool for automating the deployment and management of infrastructure. In the stock data analysis project, Terraform is used to create the necessary resources on Google Cloud Platform (GCP), including a GCP storage bucket and a BigQuery dataset.

To create these resources using Terraform, you first define the required infrastructure in a Terraform configuration file. This includes defining the GCP project, creating the storage bucket, and creating the BigQuery dataset. You can also specify any additional configuration, such as access control policies.

Once the configuration file is defined, you can use the terraform apply command to deploy the resources on GCP. Terraform will automatically create the necessary resources and configure them according to the specifications in the configuration file.

By using Terraform in this way, you can easily and consistently create the required infrastructure for the stock data analysis project. This provides a scalable and repeatable solution for managing the necessary resources on GCP. It is assumed that the user is familiar with the basics of Terraform and GCP in order to understand how the infrastructure is being created and managed.

2. <b>GCP</b> (BigQuery and Google Cloud Storage) - Used to store and process large amounts of data for the stock data analysis project. BigQuery is used to store and query the stock data, while Google Cloud Storage is used to store the raw data before it is transformed.

3. <b>Airflow</b> - Used to orchestrate the ETL (extract, transform, load) pipeline for the stock data analysis project. Airflow is used to schedule and execute the data transformation jobs using dbt.

<i>Instructions</i>
To load the data into GCS, an Airflow DAG is used along with a Python script that extracts data from the Kaggle dataset API and loads it into GCS. This script is scheduled to run periodically using Airflow, allowing for regular updates to the raw data.

Once the raw data is stored in GCS, another script is used to load the data into BigQuery using a similar approach. This involves defining a BigQuery table schema and using a Python script to load the data from GCS into the corresponding BigQuery table.

By using GCS in this way, the stock data analysis project is able to store and manage large amounts of raw data in a scalable and cost-effective manner. The use of Airflow and Python scripts streamlines the ETL process, allowing for regular updates to the data and efficient loading into BigQuery. This enables efficient querying and analysis of the data in the next stages of the project.

4. <b>dbt</b> - Used to transform the raw stock data into a format that is optimized for analysis. dbt is used to model the data and build a data warehouse in BigQuery, allowing for efficient querying and analysis.

<i>Instructions</i>
dbt, or Data Build Tool, is a popular open-source data transformation tool that allows users to define data transformation logic in SQL code. In the stock data analysis project, dbt is used to transform the raw data stored in BigQuery into a more structured and organized dataset that is easier to query and analyze.

In addition to transforming the raw data, dbt is also used to enrich the dataset by adding additional data sources. For example, data from NASDAQ is extracted to add information on sectors, stock names, and industries, providing more context and insights into the stock data.

By using dbt in this way, the stock data analysis project is able to quickly and efficiently transform and enrich the dataset using SQL code. This provides a structured and organized dataset that is easy to query and analyze, and includes additional information on sectors, stock names, and industries.

5. <b>Power BI</b> - Used to create the final dashboard for the stock data analysis project. Power BI is used to create two charts: a line chart showing day-to-day stock performance and a bar chart showing the top 5 sectors in the USA market. Power BI is also used to create visualizations and provide interactive filtering and slicing of the data.

