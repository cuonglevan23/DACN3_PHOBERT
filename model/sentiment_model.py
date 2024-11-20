from transformers import pipeline
import re
from collections import Counter

# Mô hình và ánh xạ nhãn
model_name = "levancuong17/DACN3_LVC"
classifier = pipeline("text-classification", model=model_name, tokenizer=model_name)

label_mapping = {
    "LABEL_0": "Thích thú",
    "LABEL_1": "Ghê tởm",
    "LABEL_2": "Khác",
    "LABEL_3": "Buồn bã",
    "LABEL_4": "Giận dữ",
    "LABEL_5": "Sợ hãi",
    "LABEL_6": "Ngạc nhiên"
}

# Hàm tách câu
def split_sentences(text):
    sentences = re.split(r'[.!?;]', text)  # Tách câu theo dấu ngắt câu
    sentences = [s.strip() for s in sentences if s.strip()]  # Loại bỏ khoảng trắng và câu rỗng
    return sentences

# Hàm phân tích cảm xúc
def analyze_comments(comments):
    results = []
    for comment in comments:
        try:
            sentences = split_sentences(comment)
            details = []

            # Phân tích cảm xúc từng câu
            for sentence in sentences:
                if len(sentence) > 512:  # Xử lý câu dài
                    sentence = sentence[:512]
                prediction = classifier(sentence)

                # Lấy nhãn cảm xúc
                if prediction:
                    emotion = label_mapping.get(prediction[0]['label'], "Không xác định")
                    details.append({"sentence": sentence, "emotion": emotion})

            # Tổng hợp cảm xúc chính
            if details:
                overall_emotion = Counter([d["emotion"] for d in details]).most_common(1)[0][0]
                results.append({"comment": comment, "emotion": overall_emotion, "details": details})

        except Exception as e:
            print(f"Error processing comment '{comment}': {e}")

    return results
