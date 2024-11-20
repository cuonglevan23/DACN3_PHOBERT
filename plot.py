import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
from wordcloud import WordCloud

def plot_emotion_distribution(analysis_results):
    # Tạo danh sách cảm xúc từ kết quả phân tích
    emotions = [result['emotion'] for result in analysis_results]
    emotion_counts = pd.Series(emotions).value_counts()

    # Biểu đồ phân phối cảm xúc
    plt.figure(figsize=(10, 5))
    sns.barplot(x=emotion_counts.index, y=emotion_counts.values, palette="viridis")
    plt.title("Phân phối cảm xúc của bình luận")
    plt.xlabel("Cảm xúc")
    plt.ylabel("Số lượng bình luận")
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Bảng thể hiện tổng các bình luận theo cảm xúc
    st.subheader("Tổng số bình luận theo cảm xúc:")
    emotion_summary = emotion_counts.reset_index()
    emotion_summary.columns = ['Cảm xúc', 'Số lượng bình luận']
    st.dataframe(emotion_summary)

    # Biểu đồ pie thể hiện tỷ lệ các cảm xúc
    plt.figure(figsize=(7, 7))
    emotion_counts.plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette("viridis", len(emotion_counts)))
    plt.title("Tỷ lệ phân phối cảm xúc của bình luận")
    plt.ylabel('')  # Ẩn nhãn trục y
    st.pyplot(plt)


    # Tạo Word Cloud từ tất cả các bình luận
    all_comments = " ".join([result['comment'] for result in analysis_results])  # Tạo chuỗi các bình luận
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_comments)

    # Hiển thị Word Cloud
    st.subheader("Bản đồ từ (Word Cloud)")
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")  # Ẩn trục
    st.pyplot(plt)
