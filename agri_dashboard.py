import pandas as pd
import pymysql
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# Database connection
myconnection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='1015',
    database='Agriculture'
)

# Function to fetch data from the database
def fetch_data(query):
    with myconnection.cursor() as cur:
        cur.execute(query)
        data = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
    return pd.DataFrame(data, columns=columns)


def streamlit_app():
    st.title("Agriculture Data Analysis")

    # Sample data
    df = fetch_data("SELECT * FROM agri_data;")
    st.write("Sample Data from agri_data Table:")
    st.write(df.groupby('year').head(100))

    # Key metrics
    total_records = fetch_data("SELECT COUNT(*) FROM agri_data;").iloc[0, 0]
    total_rice_yield = fetch_data("SELECT SUM(rice_yield) FROM agri_data;").iloc[0, 0] or 0
    total_wheat_yield = fetch_data("SELECT SUM(wheat_yield) FROM agri_data;").iloc[0, 0] or 0
    total_cotton_yield = fetch_data("SELECT SUM(cotton_yield) FROM agri_data;").iloc[0, 0] or 0
    total_groundnut_yield = fetch_data("SELECT SUM(groundnut_yield) FROM agri_data;").iloc[0, 0] or 0
    total_maize_yield = fetch_data("SELECT SUM(maize_yield) FROM agri_data;").iloc[0, 0] or 0

    st.subheader("Key Metrics")

    # Create a 3x2 grid of metrics
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)

    col1.metric("Total Records in agri_data", value=int(total_records))
    col2.metric("Total Rice Yield", value=f"{total_rice_yield:.2f} kg/ha")
    col3.metric("Total Wheat Yield", value=f"{total_wheat_yield:.2f} kg/ha")
    col4.metric("Total Cotton Yield", value=f"{total_cotton_yield:.2f} kg/ha")
    col5.metric("Total Groundnut Yield", value=f"{total_groundnut_yield:.2f} kg/ha")
    col6.metric("Total Maize Yield", value=f"{total_maize_yield:.2f} kg/ha")

   
    st.subheader('Top 3 years with highest rice production')
    st.write(fetch_data("SELECT year, SUM(rice_production) AS total_rice_production FROM agri_data GROUP BY year ORDER BY total_rice_production DESC LIMIT 3;"))

    wheat_top5 = df.groupby('state_name')['wheat_area'].sum().sort_values(ascending=False).head(5)
    # Bar
    wheat_top5.plot(kind='bar', color='orange')
    plt.title("Top 5 Wheat Producing States")
    plt.ylabel("Wheat Area (1000 ha)")
    plt.show()
    st.pyplot(fig=plt.gcf())
   
    st.subheader('Top 5 Districts by Wheat Yield Over the Last 5 Years')
    st.write(fetch_data("SELECT year,dist_name as district, SUM(wheat_yield) AS total_wheat_yield FROM agri_data GROUP BY year, district ORDER BY total_wheat_yield DESC LIMIT 5;"))

    st.subheader('States with the Highest Growth in Oilseed Production')
    st.write(fetch_data("SELECT state_name as state, SUM(oilseeds_production) AS total_oilseed_production FROM agri_data GROUP BY state ORDER BY total_oilseed_production DESC LIMIT 5;"))
     
    st.subheader('District-wise Correlation Between Area and Production for Major Crops (Rice, Wheat, and Maize)')
    st.write(fetch_data("SELECT dist_name as district, SUM(rice_area) AS total_rice_area, SUM(rice_production) AS total_rice_production, SUM(wheat_area) AS total_wheat_area, SUM(wheat_production) AS total_wheat_production, SUM(maize_area) AS total_maize_area, SUM(maize_production) AS total_maize_production FROM agri_data GROUP BY district;"))
    

    st.subheader('Yearly Production Growth of Cotton in Top 5 Cotton Producing States')
    st.write(fetch_data("SELECT year, state_name as state, SUM(cotton_production) AS total_cotton_production FROM agri_data GROUP BY year, state ORDER BY total_cotton_production DESC LIMIT 5;"))
   

    st.subheader('Districts with the Highest Groundnut Production in 2017')
    groundnut_production_2017 = fetch_data("SELECT dist_name as district, SUM(groundnut_production) AS total_groundnut_production FROM agri_data WHERE year = 2017 GROUP BY district ORDER BY total_groundnut_production DESC LIMIT 5;")
    st.write(groundnut_production_2017)


    st.subheader('Annual Average Maize Yield Across All States')
    st.write(df.groupby('state_name')['maize_yield'].mean())


    st.subheader('Total Area Cultivated for Oilseeds in Each State')
    st.write(df.groupby('state_name')['oilseeds_area'].sum())

    st.subheader('Yearly Production Trend for Rice and Wheat')
    crop_trend = df.groupby('year')[['rice_area', 'wheat_area']].sum()
    crop_trend.plot(marker='o')
    plt.title("Rice vs Wheat Production (Last 50 Years)")
    plt.ylabel("Area (1000 ha)")
    plt.show()
    st.pyplot(fig=plt.gcf())

    


    st.subheader('Districts with the Highest Rice Yield')
    st.write(df.groupby('dist_name')['rice_yield'].sum().sort_values(ascending=False).head(10))

   



    
if __name__ == "__main__":
    streamlit_app()