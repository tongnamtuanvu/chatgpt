import { OpenAI } from "openai";
import * as pd from "pandas";
import * as time from "time";

console.log("Metricity");

#ketnoi api chatgpt

const client = new OpenAI({ api_key: "<your_api_key>" });

let openai_model = "gpt-4";
let messages: any[] = [];

let file_data: string = "";

//upload file len

function uploadCSVFile(file: any) {
    const data = pd.read_csv(file);
    file_data = data.toString();
    console.log(data);
}

function handleUserInput(prompt: string) {
    if (file_data !== "") {
        messages.push({
            "role": "user",
            "content": "searching on data : " + file_data + "and answer question from user : " + prompt + ". If there aren't any question related to data, you don't need to base on it, just answer base on what you know"
        });
    } else {
        messages.push({
            "role": "user",
            "content": prompt
        });
    }

    console.log(prompt);
}


function handleCompletions() {
    let full_response = "";

    for (const message of messages) {
        console.log(message.role + ": " + message.content);
    }

    client.chat.completions.create(
        {
            model: openai_model,
            messages: messages.map(m => ({
                "role": m.role,
                "content": m.content
            })),
            stream: true
        },
        (response: any) => {
            full_response += (response.choices[0].delta.content || "");
            console.log(full_response);
        }
    );

    messages.push({
        "role": "assistant",
        "content": full_response
    });
}


const uploaded_file = "<uploaded_csv_file_path>";
uploadCSVFile(uploaded_file);

const user_input = "Example user input";
handleUserInput(user_input);


handleCompletions();
