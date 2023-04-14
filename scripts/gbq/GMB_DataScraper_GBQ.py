import datetime
import time
from datetime import datetime
import pandas as pd
import numpy as np
import os
from google.cloud import bigquery


class GBQ:
    @staticmethod
    def gbq_api_call(split_on_pipe_list, account_id, location_id, date_prev_month):
        # Assign account_id and location_id values.
        search_query = split_on_pipe_list[1::3]
        volume = split_on_pipe_list[2::3]
        # Assign Search query results a column name - 'Search query'.
        df_column_search_queries = pd.DataFrame(search_query, columns=['search_query'])
        # lambda expression for find/replace a comma with emtpy space, avoid a new line.
        df_column_search_queries['search_query'] = [x.replace(',', '') for x in
                                                    df_column_search_queries['search_query']]
        # Assign Volume data column a name - 'Volume'.
        df_column_volume = pd.DataFrame(volume, columns=['volume'])
        # Actions to remove empty spaces and comparison operators from origin dataframe.
        df_column_volume["volume"] = df_column_volume["volume"].str.replace(" ", "")
        df_column_volume["volume"] = df_column_volume["volume"].str.replace("<", "")
        df_column_volume["volume"] = df_column_volume["volume"].str.replace(">", "")
        df_column_volume["volume"] = df_column_volume["volume"].str.strip()
        # Generate date time in custom format dd-MM-yyyy HH:mm:ss.
        # Concatenate the Search query, Volume and Date dataframes into a single df.
        df_search_queries_volume = pd.concat([df_column_search_queries, df_column_volume], axis=1)
        # Insert Date and Group data inside end dataframe structure.
        df_search_queries_volume['date'] = df_search_queries_volume['search_query'].apply(lambda x: date_prev_month)
        df_search_queries_volume['account_id'] = df_search_queries_volume['search_query'].apply(
            lambda y: account_id)
        df_search_queries_volume['location_id'] = df_search_queries_volume['search_query'].apply(
            lambda y: location_id)
        # Convert current datetime from string into datetime in the format yyyy-MM-dd HH:MM:SS
        date_string = time.strftime('%Y-%m-%d %H:%M:%S')
        date_time_loaded = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        df_search_queries_volume['_time_loaded'] = df_search_queries_volume['search_query'].apply(
            lambda x: date_time_loaded).astype(str)

        # API Configuration.
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.dirname(
            os.path.abspath(__file__)) + "\service_account.json"
        client = bigquery.Client()
        table_id = "test_dataset.search_queries_test"
        # table_id = "test_dataset.search_queries_raw"

        # Split data size into 1 equal chunks of data, load the data straight from DataFrame into BigQuery (gbq-API).
        for data in np.array_split(df_search_queries_volume, 1):
            job_config = bigquery.LoadJobConfig(schema=[
                bigquery.SchemaField("search_query", bigquery.enums.SqlTypeNames.STRING),
                bigquery.SchemaField("volume", bigquery.enums.SqlTypeNames.STRING),
                bigquery.SchemaField("date", bigquery.enums.SqlTypeNames.STRING),
                bigquery.SchemaField("account_id", bigquery.enums.SqlTypeNames.STRING),
                bigquery.SchemaField("location_id", bigquery.enums.SqlTypeNames.STRING),
                bigquery.SchemaField("_time_loaded", bigquery.enums.SqlTypeNames.STRING),
            ])

            # Append the data at each iteration.
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
            job = client.load_table_from_dataframe(data, table_id, job_config=job_config)
            job.result()
            # End timestamp.
            # end_time = start_time - datetime.now()
            # logger.info(f"End time for each month after upload to gbq: {end_time}")