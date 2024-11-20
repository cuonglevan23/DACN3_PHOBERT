import streamlit as st
from utils.youtube_api import get_video_comments, get_video_info
from model.sentiment_model import analyze_comments
from plot import plot_emotion_distribution

# Điều hướng trang
page = st.sidebar.selectbox("Chọn trang", ["Phân tích bình luận", "Biểu đồ phân phối cảm xúc"])

# Khởi tạo session_state
if 'video_info' not in st.session_state:
    st.session_state.video_info = None
if 'comments' not in st.session_state:
    st.session_state.comments = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'video_url' not in st.session_state:
    st.session_state.video_url = ''
if 'blurred' not in st.session_state:
    st.session_state.blurred = False  # Track if comments should be blurred

# Trang phân tích bình luận
if page == "Phân tích bình luận":
    st.title("Ứng dụng Phân tích Video YouTube")

    # Nhập URL và số lượng bình luận
    video_url = st.text_input("Nhập URL video YouTube:", st.session_state.video_url)
    num_comments = st.selectbox("Số lượng bình luận muốn lấy:", options=[20, 50, 100], index=2)

    if st.button("Phân tích bình luận"):
        st.session_state.video_url = video_url  # Lưu URL vào session_state
        st.session_state.video_info = get_video_info(video_url)
        st.session_state.comments = get_video_comments(video_url, max_comments=num_comments)
        st.session_state.analysis_results = analyze_comments(st.session_state.comments)
        st.session_state.blurred = False  # Reset blur state when re-analyzing

    # Hiển thị thông tin và kết quả phân tích
    if st.session_state.video_info:
        st.subheader("Thông tin video:")
        st.write(f"Tiêu đề: {st.session_state.video_info['title']}")
        st.write(f"Số lượt xem: {st.session_state.video_info['view_count']}")
        st.write(f"Số bình luận: {st.session_state.video_info['comment_count']}")
        st.video(st.session_state.video_url)

    # Hiển thị bình luận và chi tiết
    if st.session_state.analysis_results:
        # Toggle nút để làm mờ/hiển thị bình luận
        if st.button("Làm mờ bình luận"):
            st.session_state.blurred = not st.session_state.blurred

        # Lọc cảm xúc
        st.subheader("Phân tích cảm xúc bình luận:")
        unique_emotions = ["Tất cả"] + list({result['emotion'] for result in st.session_state.analysis_results})
        selected_emotion = st.selectbox("Chọn cảm xúc để lọc bình luận:", unique_emotions)

        for result in st.session_state.analysis_results:
            # Lọc theo cảm xúc được chọn
            if selected_emotion != "Tất cả" and result['emotion'] != selected_emotion:
                continue

            # Làm mờ nếu là cảm xúc "Giận dữ" và trạng thái blur đang bật
            if result['emotion'] == "Giận dữ" and st.session_state.blurred:
                comment_text = "**[Bình luận đã làm mờ]**"
            else:
                comment_text = f"**{result['comment']}**"

            # Hiển thị cảm xúc chính
            st.write(f"{comment_text} - Cảm xúc chính: {result['emotion']}")

            # Hiển thị chi tiết từng câu
            with st.expander("Xem chi tiết từng câu"):
                for detail in result["details"]:
                    st.write(f"- **{detail['sentence']}**: {detail['emotion']}")

        st.write(f"Tổng số bình luận đã phân tích: {len(st.session_state.comments)}")


# Trang biểu đồ phân phối cảm xúc
elif page == "Biểu đồ phân phối cảm xúc":
    st.title("Biểu đồ Phân phối Cảm xúc")
    if st.session_state.analysis_results:
        plot_emotion_distribution(st.session_state.analysis_results)
    else:
        st.write("Chưa có dữ liệu để hiển thị biểu đồ. Vui lòng phân tích bình luận trước.")
