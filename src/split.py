from dotenv import load_dotenv
import os
import google.generativeai as genai

# GEMINI_API_KEY = None

def setup_env():
    load_dotenv()
    global GEMINI_API_KEY
    GEMINI_API_KEY = os.getenv("API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"Error reading the file '{file_path}': {str(e)}")
        return None

def gen_text(): 
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    absolute_path = os.path.abspath('.')
    
    prompt_file = "prompts/step_1.txt"
    prompt_path = os.path.join(absolute_path, prompt_file)
    
    text_file = "text/BTC.107254/content.txt"
    text_path = os.path.join(absolute_path, text_file)

    text = read_text_file(text_path)
    prompt = read_text_file(prompt_path)

    prompt = prompt + "\n" + text\
    
    # print(prompt)

    response = model.generate_content(prompt)
    print(response)

if __name__ == "__main__":
    setup_env()

    gen_text()

