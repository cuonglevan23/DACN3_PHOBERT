from transformers import pipeline

# Tên mô hình trên Hugging Face Hub
model_name = "levancuong17/DACN3_LVC"
classifier = pipeline("text-classification", model=model_name, tokenizer=model_name)

# Từ điển ánh xạ nhãn
label_mapping = {
    "LABEL_0": "Thích thú",
    "LABEL_1": "Ghê tởm",
    "LABEL_2": "Khác",
    "LABEL_3": "Buồn bã",
    "LABEL_4": "Giận dữ",
    "LABEL_5": "Sợ hãi",
    "LABEL_6": "Ngạc nhiên"
}


def analyze_comments(comments):
    results = []
    for comment in comments:
        # Cắt bớt nếu chiều dài comment vượt quá 512
        if len(comment) > 512:
            comment = comment[:512]

        try:
            # Dự đoán cảm xúc
            prediction = classifier(comment)

            # Kiểm tra dự đoán có trả về kết quả không
            if not prediction:
                continue

            # Ánh xạ nhãn dự đoán
            label = label_mapping.get(prediction[0]['label'], "Không xác định")
            results.append({"comment": comment, "emotion": label})

        except Exception as e:
            print(f"Error processing comment '{comment}': {e}")

    return results




