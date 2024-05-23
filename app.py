import pandas as pd
import streamlit as st
import matplotlib  as plt
import helper  



def remove_notification(user_list):
    if 'whatsapp notification' in user_list:
        user_list.remove('whatsapp notification')


st.sidebar.title('File Upload 📂')
uploaded_file_id = st.sidebar.file_uploader("Upload Files", type=["csv", "txt"], key="file_uploader_1")


if uploaded_file_id is not None:
    df = pd.read_csv(uploaded_file_id)
    st.title('WhatsApp Chat Analyzer 📱💬')

   
    plot_type = st.sidebar.selectbox("Select plot type 📊", ["Line Chart", "Bar Chart", "Pie Chart", "Scatter Plot"])


    if plot_type == 'Line Chart':
        y_column = st.selectbox("Select column for y-axis", df.columns)
        st.write(f"### Line Chart 📈 : {y_column}")
        st.line_chart(df[y_column])

    elif plot_type == 'Pie Chart':
        category_column = st.selectbox("Select column for categories", df.columns)
        if st.button("Generate Pie Chart"):
            st.write(f"### Pie Chart : {category_column}")
            fig, ax = plt.subplots()
            df[category_column].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
            st.pyplot(fig)

    elif plot_type == "Scatter Plot":
        x_column = st.selectbox("Select column for x-axis", df.columns)
        y_column = st.selectbox("Select column for y-axis", df.columns)
       
        if st.button("Generate Scatter Plot"):
            st.write(f"### Scatter Plot ⚪ : {x_column} vs {y_column}")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(df[x_column], df[y_column])
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            ax.set_title(f'Scatter Plot: {x_column} vs {y_column}')
            st.pyplot(fig)

    elif plot_type == "Bar Chart":
        bar_column = st.selectbox("Select column for bar chart", df.columns)
     
        if st.button("Generate Bar Chart"):
            st.write(f"### Bar Chart 📊: {bar_column}")
            plt.figure(figsize=(10, 6))
            df[bar_column].value_counts().plot(kind='bar')
            plt.xlabel(bar_column)
            plt.ylabel("Frequency")
            plt.title(f'Bar Chart: {bar_column}')
            plt.xticks(rotation=45)
            st.pyplot(plt.gcf())

    user_list = df['user'].unique().tolist()
    remove_notification(user_list)
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis ", user_list)

 
    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_msgs, links = helper.fetch_stats(selected_user, df)

        st.title('Analysis Results:')
        st.write(f"Total Messages: {num_messages}")
        
   

    if 'df' in locals():  
        total_users = df['user'].nunique()
        total_messages = df.shape[0]

        st.sidebar.write("### Summary")
        st.sidebar.write(f"Total Users: {total_users}")
        st.sidebar.write(f"Total Messages: {total_messages}")
