import time
import streamlit as st
from openai import OpenAI
import pandas as pd
import plotly.express as px

st.title("Metricity - Python version")

client = OpenAI(api_key=st.secrets["api_openai"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []

file_data = ""
uploaded_file = st.file_uploader("Upload your CSV file here")

if uploaded_file is not None:
    file = pd.read_csv(uploaded_file)
    file_data = file.to_string()

    st.write(file)

    num_rows, num_columns = file.shape

    if num_columns >= 3:
        title = "Chart for " + file.columns[1]
        # Line chart
        line_chart = px.line(file, x=file.columns[0], y=file.columns[1], title=title)
        st.plotly_chart(line_chart)
        title2 = "Chart for " + file.columns[5]
        # Bar chart
        bar_chart = px.bar(file, x=file.columns[5], y=file.columns[1], title=title2)
        st.plotly_chart(bar_chart)

        # Circle (Pie) chart
        title_pie = "Pie Chart for " + file.columns[1]
        pie_chart = px.pie(file, names=file.columns[1], title=title_pie)
        st.plotly_chart(pie_chart)

        with st.spinner('Thinking...'):
            time.sleep(15)

        if "prompt_displayed" not in st.session_state:
            st.session_state.prompt_displayed = True

            prompt = "Hãy phân tích xem dữ liệu này nói về cái gì, các con số thể hiện ra sao, từ đó chúng ta có thể thấy được điều gì?"

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": prompt + file_data
                }
            )

            with st.spinner('Thinking...'):
                full_response = ""
                holder = st.empty()

                for response in client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {
                                "role": m["role"],
                                "content": m["content"]
                            }
                            for m in st.session_state.messages
                        ],
                        stream=True,
                ):
                    full_response += (response.choices[0].delta.content or "")
                    holder.markdown(full_response + "_")
                    holder.markdown(full_response)
                holder.markdown(full_response)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response
                }
            )

if prompt := st.chat_input("Input here..."):
    if file_data != "":
        st.session_state.messages.append(
            {
                "role": "user",
                "content": "searching on data : " + file_data + "and answer question from user : " + prompt + ". If there aren't any question related to data, you don't need to base on it, just answer base on what you know"
            }
        )
    else:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

    with st.chat_message('user'):
        st.markdown(prompt)

    with st.spinner('Thinking...'):
        full_response = ""
        holder = st.empty()

        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {
                    "role": m["role"],
                    "content": m["content"]
                }
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            holder.markdown(full_response + "_")
            holder.markdown(full_response)
        holder.markdown(full_response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )
