import time
import streamlit as st
import numpy as np
import pandas as pd


# informations
captions = ["剛開學了!你正準備在前往教室的路上⋯⋯", 
            "離下堂課還有半小時,你先去學校圖書館坐著等上課,偶然發現一本你學習領域的書⋯⋯",
            "課堂小組討論中,有個成員的想法與團隊相差很大⋯",
            "終於快結束一天的課,你和朋友打算一起去餐酒館吃晚餐跟小酌幾杯⋯⋯",
            "你和朋友都點好餐了,結果服務人員上錯餐了，",
            "幾杯黃湯下肚後,話題越來越深層",
            "一位朋友向你吐露心事,提到他們最近的困難⋯⋯",
            "結束沈重的話題,你和朋友決定下週末一起去台東兩天一日遊！"]
questions = {
    # EI
    "在走廊遇到你不熟的同學,你的反應是⋯⋯?": {
        "熱情打招呼、小聊幾句": 0.5,
        "主動微笑點頭經過": 0.2,
        "對方打招呼才會回應": -0.2,
        "假裝沒看到或滑手機裝忙": -0.5
    },
    # SN
    "你會怎麼做?": {
        "尋找能應用的知識或技巧": 0.5,
        "閱讀書本中未來可能性的探討": -0.5,
        "隨意翻翻，沒有特別往哪方面閱讀": -0.2
    },
    #TF
    "你會怎麼處理?": {
        "客觀分析,指出其想法的漏洞,尋求最有效的解決方案": 0.3,
        "嘗試理解他的感受,尋求一個能讓大家都滿意的妥協方案": -0.3
    },
    #JP
    "你會⋯⋯?": {
        "先定好餐廳,以免撲空": 0.5,
        "隨機應變,如果客滿再找其他的也沒關係": -0.5
    },
    #EI
    "上成你不想吃的餐，你會⋯⋯?": {
        "請他重上一份正確的餐點": 0.6, 
        "算了⋯⋯還要換餐蠻麻煩的": -0.5
    },
    # SN
    "你和朋友聊到另一半的選擇，你認為⋯⋯?": {
        "沒有麵包的愛情就是一盤散沙！": 0.7,
        "愛情能克服困難的！": -0.7
    },
    # TF
    "你如何回應?": {
        "注重問題解決,提供具體建議和解決策略": 0.5,
        "注重感受層面,傾聽並給予情感支持": -0.5
    },
    # JP
    "你的角色是?": {
        "主力規劃出遊的大小事": 0.5,
        "作為團內吉祥物": 0.3,
        "負責一些沒被規劃的事情": -0.5
    }
}
place_image = {
    "Q1_Q": "https://imgur.com/mzvtdAS.png",  # for Q2
    "Q1_A1": "https://imgur.com/mzvtdAS.png",  # for Q1 options
    "Q1_A2": "https://imgur.com/mzvtdAS.png", 
    "Q1_A3": "https://imgur.com/mzvtdAS.png", 
    "Q1_A4": "https://imgur.com/mzvtdAS.png",  

    "Q2_Q": "https://imgur.com/mzvtdAS",  # for Q2
    "Q2_A1": "https://imgur.com/mzvtdAS",  # for Q2 options
    "Q2_A2": "https://imgur.com/mzvtdAS", 
    "Q2_A3": "https://imgur.com/mzvtdAS", 

    "Q3_Q": "https://imgur.com/mzvtdAS",  # for Q3
    "Q3_A1": "https://imgur.com/mzvtdAS",  # for Q3 options
    "Q3_A2": "https://imgur.com/mzvtdAS", 

    "Q4_Q": "https://imgur.com/mzvtdAS",  # for Q4
    "Q4_A1": "https://imgur.com/mzvtdAS",  # for Q4 options
    "Q4_A2": "https://imgur.com/mzvtdAS",

    "Q5_Q": "https://imgur.com/mzvtdAS",  # for Q5
    "Q5_A1": "https://imgur.com/mzvtdAS",  # for Q5 options
    "Q5_A2": "https://imgur.com/mzvtdAS",

    "Q6_Q": "https://imgur.com/mzvtdAS",  # for Q6
    "Q6_A1": "https://imgur.com/mzvtdAS",  # for Q6 options
    "Q6_A2": "https://imgur.com/mzvtdAS",

    "Q7_Q": "https://imgur.com/mzvtdAS",  # for Q7
    "Q7_A1": "https://imgur.com/mzvtdAS",  # for Q7 options
    "Q7_A2": "https://imgur.com/mzvtdAS",

    "Q8_Q": "https://imgur.com/mzvtdAS",  # for Q8
    "Q8_A1": "https://imgur.com/mzvtdAS",  # for Q8 options
    "Q8_A2": "https://imgur.com/mzvtdAS",
    "Q8_A3": "https://imgur.com/mzvtdAS", 



}
questions_info = [
    {
        "caption": captions[0], 
        "question": "在走廊遇到你不熟的同學,你的反應是⋯⋯?",
        "options": ["熱情打招呼、小聊幾句", "主動微笑點頭經過", "對方打招呼才會回應", "假裝沒看到或滑手機裝忙"]
    },
    {
        "caption": captions[1], 
        "question": "你會怎麼做?",
        "options": ["尋找能應用的知識或技巧", "閱讀書本中未來可能性的探討", "隨意翻翻，沒有特別往哪方面閱讀"]
    },
    {
        "caption": captions[2], 
        "question": "你會怎麼處理?",
        "options": ["客觀分析,指出其想法的漏洞,尋求最有效的解決方案", "嘗試理解他的感受,尋求一個能讓大家都滿意的妥協方案"]
    },
    {
        "caption": captions[3], 
        "question": "你會⋯⋯?",
        "options": ["先定好餐廳,以免撲空", "隨機應變,如果客滿再找其他的也沒關係"]
    },
    {
        "caption": captions[4], 
        "question": "上成你不想吃的餐，你會⋯⋯?",
        "options": ["請他重上一份正確的餐點", "算了⋯⋯還要換餐蠻麻煩的"]
    },
    {
        "caption": captions[5], 
        "question": "你和朋友聊到另一半的選擇，你認為⋯⋯?",
        "options": ["沒有麵包的愛情就是一盤散沙！", "愛情能克服困難的！"]
    },
    {
        "caption": captions[6], 
        "question": "你如何回應?",
        "options": ["注重問題解決,提供具體建議和解決策略", "注重感受層面,傾聽並給予情感支持"]
    },
    {
        "caption": captions[-1], 
        "question": "你的角色是?",
        "options": ["主力規劃出遊的大小事", "作為團內吉祥物", "負責一些沒被規劃的事情"]
    }
]

# personality descriptions
personality_trans = {
    "ESP": "百變觔斗雲",
    "ISP": "隱形水汽雲",
    "ESJ": "堅定積雲",
    "ISJ": "守護層雲",
    "ENJ": "智慧高層雲",
    "INJ": "深思冰晶雲",
    "ENP": "夢想彩虹雲",
    "INP": "靈魂霧雲"
}
## transform
personality_descriptions = {
    "百變觔斗雲": "像觔斗雲一樣多變和充滿能量，你喜歡探索和享受刺激，並能夠迅速適應變化，充滿活力和創造力。",
    "隱形水汽雲": "隱形水汽雲蘊含著靜默的力量，你喜歡在背後默默地探索和創造，具有深度的思考和藝術感，但往往不顯山不露水。",
    "堅定積雲": "堅定積雲，堅實可靠，覆蓋廣泛，你是群體中的中流砥柱，並以堅定和可靠性為他人所尊敬，擅長維繫社會秩序及和諧。",
    "守護層雲": "守護層雲，穩定而廣泛，你是規則的守護者，默默守護著社會價值，確保一切按計劃進行，提供安全和安寧。",
    "智慧高層雲": "高層雲遠見和洞察，你是天生的領導者，並擁有遠大的視野和創新思維，積極尋求超越現狀的方法。",
    "深思冰晶雲": "冰晶雲，高遠而複雜，你善於深度思考和自我省思，喜歡探索理論和概念，追求知識和真理。",
    "夢想彩虹雲": "彩虹雲，多彩和充滿希望，你善於激勵和鼓舞人心，並擁有強大的感染力，能夠激勵他人追隨他們的夢想和理想。",
    "靈魂霧雲": "霧雲，神秘和內在的，你是個深藏不漏且富有同情心的人，並深刻理解人性，追求內在和諧與世界的美好。"
}

# initialize page
if 'page' not in st.session_state:
    st.session_state['page'] = 0
    st.session_state['scores'] = {"ei": 0, "sn": 0, "jp": 0}
    st.session_state['progress'] = 0

# Define a function for updating scores and moving to the next question
def next_page(selected_option=None, question_number=None):
    if selected_option is not None and question_number is not None:
        if question_number in [1, 5]:
            dimension = "ei"
        elif question_number in [2, 6]:
            dimension = "sn"
        elif question_number in [4, 8]:
            dimension = "jp"
        else:
            return  
        st.session_state.scores[dimension] += selected_option
    # 進度條
    st.session_state.progress = min(st.session_state.progress + 1/len(captions), 1)
    st.session_state.page += 1 

# Function to go back to the previous question/page
def go_back():
    if st.session_state.page > 1:
        st.session_state.page -= 1

# calculate score
def calculate_personality_type():
    personality_type = ""
    personality_type += "E" if st.session_state.scores["ei"] >= 0 else "I"
    personality_type += "S" if st.session_state.scores["sn"] >= 0 else "N"
    personality_type += "J" if st.session_state.scores["jp"] >= 0 else "P"
    return personality_type

# show progress
progress_bar = st.progress(st.session_state.progress)

# page1: info
if st.session_state.page == 0:
    st.title("你是哪種雲？")
    st.write("這是一個關於日常生活選擇的性格測試。填Google表單。")
                
    # google form link
    form_url = "https://forms.gle/Y8kTAwtLYtqKumdn6"
    st.markdown(f"[請填寫]({form_url})", unsafe_allow_html=True)
                
    if st.button("開始測試"):
        next_page()

# page 2-9
elif 1 <= st.session_state.page <= len(questions):
    index = st.session_state.page-1
    st.subheader(captions[index])
    st.image(place_image[f"Q{index+1}_Q"], width=300)
    q = questions_info[index]['question']
    st.write(q)

    cols = st.columns(len(questions_info[index]["options"]))
    for i, option in enumerate(questions_info[index]["options"], start=1):
        weight = questions[q][option]
        with cols[i-1]:
            img_key = f"Q{index+1}_A{i}"
            st.image(place_image[img_key], width=100)
            if st.button(option, key=f'Q{index}_A{i}'):
                next_page(selected_option=weight, question_number=i)
    if st.session_state.page > 1:
        st.button("上一題", on_click=go_back)
# page10: ending
elif st.session_state.page == len(questions) + 1:
    personality_type = calculate_personality_type()
    personality_transform = personality_trans[personality_type]
    description = personality_descriptions[personality_transform]
    st.subheader(f"你是 {personality_transform}")
    st.write(description)
    if st.button("是的，發送到我的郵箱"):
        st.write("結果已發送！")
    elif st.button("再一次！"):
        st.session_state.page = 0
        st.session_state.scores = {"ei": 0, "sn": 0, "jp": 0}
