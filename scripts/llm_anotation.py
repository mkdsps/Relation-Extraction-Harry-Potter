#anotira paragrafe koje mu prosledis...
def anotate_paragraphs(paragraphs: list, * ,model: str = 'gpt-4.1-mini')-> list:
    
    import json
    from helper_classes import Output
    from openai import OpenAI
    from dotenv import load_dotenv
    import os

    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')

    client = OpenAI(api_key=api_key) 
    
    messages = build_annotation_prompt(paragraphs)
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=messages,
        response_format=Output
    )
    return  json.loads(completion.choices[0].message.content)    

# def rebuild(paragraphs: list[dict]) -> list[dict]:
#   for paragraph in paragraphs:
#     paragraph['tokens'] = [[i,x] for i,x in enumerate(paragraph['tokens'])]
#   return paragraphs

def build_annotation_prompt(paragraphs: list) -> str:
    with open('../prompts/prompt_final.txt', 'r') as file:
      prompt = file.read()

    return [
    {
        "role": "system",
        "content": "You are an expert NLP annotator for the Harry Potter book series."
    },
    {
        "role": "user",
        "content": prompt + f"\n{paragraphs}"
    }
]


if __name__ == '__main__':
    import json

    your_paragraphs = [
    {
      "id": 6,
      "tokens": ['‘', 'Natural', '##ly', ',', '’', 'said', 'Professor', 'M', '##c', '##G', '##ona', '##gall', '.', '‘', 'James', 'Potter', 'told', 'Du', '##mble', '##dor', '##e', 'that', 'Black', 'would', 'die', 'rather', 'than', 'tell', 'where', 'they', 'were', ',', 'that', 'Black', 'was', 'planning', 'to', 'go', 'into', 'hiding', 'himself', '…', 'and', 'yet', ',', 'Du', '##mble', '##dor', '##e', 'remained', 'worried', '.', 'I', 'remember', 'him', 'offering', 'to', 'be', 'the', 'Potter', '##s', '’', 'Secret', '-', 'Keeper', 'himself', '.', '’']
    },
    {
      "id": 523,
      "tokens": ['“', 'We', 'won', '!', 'You', 'won', '!', 'We', 'won', '!', '”', 'shouted', 'Ron', ',', 'thump', '##ing', 'Harry', 'on', 'the', 'back', '.', '“', 'And', 'I', 'gave', 'Mal', '##fo', '##y', 'a', 'black', 'eye', ',', 'and', 'Neville', 'tried', 'to', 'take', 'on', 'C', '##rab', '##be', 'and', 'Go', '##yle', 'single', '-', 'handed', '!', 'He', '’', 's', 'still', 'out', 'cold', 'but', 'Mad', '##am', 'Po', '##m', '##frey', 'says', 'he', '’', 'll', 'be', 'all', 'right', '—', 'talk', 'about', 'showing', 'S', '##ly', '##ther', '##in', '!', 'I', '’', 've', 'waiting', 'for', 'you', 'in', 'the', 'common', 'room', ',', 'we', '’', 're', 'having', 'a', 'party', ',', 'Fred', 'and', 'George', 'stole', 'some', 'cakes', 'and', 'stuff', 'from', 'the', 'kitchen', '##s', '.', '”']
    },
    {
        "id": 232,
        "tokens": ['God', '##ric', 'G', '##ry', '##ffin', '##dor', '“', 'Only', 'a', 'true', 'G', '##ry', '##ffin', '##dor', 'could', 'have', 'pulled', 'that', 'out', 'of', 'the', 'hat', ',', 'Harry', ',', '”', 'said', 'Du', '##mble', '##dor', '##e', 'simply', '.', 'For', 'a', 'minute', ',', 'neither', 'of', 'them', 'spoke', '.', 'Then', 'Du', '##mble', '##dor', '##e', 'pulled', 'open', 'one', 'of', 'the', 'drawers', 'in', 'Professor', 'M', '##c', '##G', '##ona', '##gall', '’', 's', 'desk', 'and', 'took', 'out', 'a', 'q', '##uil', '##l', 'and', 'a', 'bottle', 'of', 'ink', '.']
    }
    ]
    data = anotate_paragraphs(your_paragraphs)
    with open('output.json', 'w') as f:
      json.dump(data, f, indent=1)