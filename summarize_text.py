import os
import google.generativeai as genai

# Set the API key
genai.configure(api_key="AIzaSyCvLXwplzhhhqybZ6jb8Ot7VIWLB3C8yig")


def summarize_text(text, lang='en'):
    model = genai.GenerativeModel("gemini-1.5-pro")

    prompt = f"""
    The following text is in its original language. Provide the output in this language: {lang}.
    
    Format the output as follows:
    
    Summary:
    short summary of the video
    
    Key Takeaways:
    succinct bullet point list of key takeaways
    
    Input text: {text}
    """

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    text_to_summarize = input("Enter the text to summarize: ")
    lang = input("Enter the language for the summary: ")
    summary = summarize_text(text_to_summarize, lang)
    print("Summary:")
    print(summary)
