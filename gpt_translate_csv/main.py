import csv

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def translate(text: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert translating English to Chinese. You need to translate the following sentence from English to Chinese, and keep the original formatting."},
            {
                "role": "user",
                "content": text
            }
        ]
    )
    translated_text = completion.choices[0].message.content
    return translated_text if translated_text else ""


if __name__ == "__main__":
    new_csv = []
    with open("example.csv", "r") as file:
        reader = csv.reader(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        for row in reader:
            new_row = []
            for cell in row:
                new_cell = translate(cell) if cell else cell
                print(f"Translating: {cell} -> {new_cell}")
                new_row.append(new_cell)
            new_csv.append(new_row)
    with open("translated.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(new_csv)
