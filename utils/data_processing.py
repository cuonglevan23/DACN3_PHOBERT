import re
import string


def clean_comment(comment):
    """Làm sạch bình luận bằng cách loại bỏ ký tự đặc biệt và chuyển đổi về chữ thường."""
    # Loại bỏ các ký tự đặc biệt và chuyển đổi về chữ thường
    comment = comment.lower()  # Chuyển về chữ thường
    comment = re.sub(r'\s+', ' ', comment)  # Thay thế nhiều khoảng trắng bằng một khoảng trắng
    comment = re.sub(r'[{}]+'.format(re.escape(string.punctuation)), '', comment)  # Loại bỏ dấu câu
    return comment.strip()


def normalize_comments(comments):
    """Chuẩn hóa danh sách bình luận."""
    return [clean_comment(comment) for comment in comments]


def categorize_emotions(results):
    """Phân loại cảm xúc từ kết quả phân tích."""
    categorized_results = {}

    for result in results:
        emotion = result['emotion']
        if emotion not in categorized_results:
            categorized_results[emotion] = []
        categorized_results[emotion].append(result['comment'])

    return categorized_results


def summarize_results(categorized_results):
    """Tóm tắt kết quả phân tích cảm xúc."""
    summary = {}
    for emotion, comments in categorized_results.items():
        summary[emotion] = len(comments)  # Đếm số lượng bình luận theo cảm xúc
    return summary
