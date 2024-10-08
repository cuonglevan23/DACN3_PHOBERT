import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from model.sentiment_model import analyze_comments
from utils.youtube_api import get_video_comments, get_video_info

st.title("Ứng dụng Phân tích Video YouTube")

# Nhập URL video YouTube
video_url = st.text_input("Nhập URL video YouTube:")

# Chọn số lượng bình luận cần lấy (20, 50, hoặc 100)
num_comments = st.selectbox("Số lượng bình luận muốn lấy:", options=[20, 50, 100], index=2)

if st.button("Phân tích bình luận"):
    # Lấy thông tin video
    video_info = get_video_info(video_url)

    # Hiển thị thông tin thống kê video
    st.subheader("Thông tin video:")
    st.write(f"Tiêu đề: {video_info['title']}")
    st.write(f"Số lượt xem: {video_info['view_count']}")
    st.write(f"Số bình luận: {video_info['comment_count']}")

    # Hiển thị video trực tiếp
    st.video(video_url)

    # Lấy bình luận từ YouTube theo số lượng yêu cầu
    comments = get_video_comments(video_url, max_comments=num_comments)

    # Phân tích cảm xúc bình luận
    analysis_results = analyze_comments(comments)

    # Thống kê cảm xúc
    emotions = [result['emotion'] for result in analysis_results]
    emotion_counts = pd.Series(emotions).value_counts()

    # Vẽ biểu đồ phân phối cảm xúc
    plt.figure(figsize=(10, 5))
    sns.barplot(x=emotion_counts.index, y=emotion_counts.values, palette="viridis")
    plt.title("Phân phối cảm xúc của bình luận")
    plt.xlabel("Cảm xúc")
    plt.ylabel("Số lượng bình luận")
    plt.xticks(rotation=45)

    # Hiển thị biểu đồ trong Streamlit
    st.pyplot(plt)

    # Hiển thị kết quả phân tích
    st.subheader("Phân tích cảm xúc bình luận:")
    for result in analysis_results:
        # Bôi đỏ bình luận ghê tởm và màu cam với bình luận sợ hãi
        if result['emotion'] == 'Ghê tởm':
            st.markdown(f"<span style='color:red; font-weight:bold;'>{result['comment']}</span> - Cảm xúc: {result['emotion']}", unsafe_allow_html=True)
        elif result['emotion'] == 'Sợ hãi':
            st.markdown(f"<span style='color:orange; font-weight:bold;'>{result['comment']}</span> - Cảm xúc: {result['emotion']}", unsafe_allow_html=True)
        elif result['emotion'] == 'Giận dữ':
            st.markdown(
                f"<span style='color:yellow; font-weight:bold;'>{result['comment']}</span> - Cảm xúc: {result['emotion']}",
                unsafe_allow_html=True)
        else:
            st.write(f"**{result['comment']}** - Cảm xúc: {result['emotion']}")

    # Hiển thị tổng số bình luận đã phân tích
    st.write(f"Tổng số bình luận đã phân tích: {len(comments)}")
