from openai import OpenAI


api_key = "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"
client = OpenAI(api_key=api_key)


# image_1 = "https://www.androidauthority.com/wp-content/uploads/2021/08/Titan-Quest-best-RPGs-for-Android.jpg"
image_1 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAA1BMVEX/AAAZ4gk3AAAASElEQVR4nO3BgQAAAADDoPlTX+AIVQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADwDcaiAAFXD1ujAAAAAElFTkSuQmCC"
image_2 = "https://upload.wikimedia.org/wikipedia/commons/e/e4/Color-blue.JPG"
response = client.chat.completions.create(
  model="gpt-4-vision-preview",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Task: tell me which colour goes with which letter."},
        {"type": "text", "text": "A:"},
        {
          "type": "image_url",
          "image_url": {
            "url": image_1,
            "detail": "high"
          },
        },
        {"type": "text", "text": "B:"},
        {
          "type": "image_url",
          "image_url": {
            "url": image_2,
            "detail": "high"
          },
        },
      ],
    }
  ],
  max_tokens=300,
  )

print(response.choices[0].message.content)