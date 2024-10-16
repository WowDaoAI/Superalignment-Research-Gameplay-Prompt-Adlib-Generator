import json
import random
import os

# Define the directory containing the JSON files
PROMPT_DIR = './prompts/'

# Load JSON files from a specific folder
def load_entities_from_folder(folder):
    entities = []
    folder_path = os.path.join(PROMPT_DIR, folder)
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            with open(os.path.join(folder_path, filename), 'r') as f:
                entities.append(json.load(f))
    return entities

# Load all necessary entities from the specified folders
countermeasures = load_entities_from_folder('countermeasures')
caught_likelihood = load_entities_from_folder('caught_likelihood')
diff_first_encounter_reasoning = load_entities_from_folder('diff_first_encounter_reasoning')
pressure = load_entities_from_folder('pressure')

# Generate a new gameplay prompt
def generate_gameplay_prompt():
    # Randomly select one entity from each category
    system_message = random.choice(countermeasures)['messages'][0]['content']
    date_message = random.choice(diff_first_encounter_reasoning)['messages'][1]['content']
    reasoning_message = random.choice(caught_likelihood)['messages'][2]['content']
    output_message = random.choice(pressure)['messages'][3]['content']

    prompt = {
        "model": "gpt-4-0613",
        "messages": [
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": date_message
            },
            {
                "role": "assistant",
                "content": reasoning_message
            },
            {
                "role": "user",
                "content": output_message
            }
        ],
        "temperature": 0.9,
        "max_tokens": 384,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    return prompt

# Save the generated prompt to a JSON file
def save_prompt_to_file(prompt, filename):
    with open(filename, 'w') as f:
        json.dump(prompt, f, indent=4)

# Main function to generate and save multiple prompts
def main(num_prompts=5):
    for i in range(num_prompts):
        prompt = generate_gameplay_prompt()
        print(f"Generated Prompt {i + 1}: {json.dumps(prompt, indent=4)}")  # Print the generated prompt
        save_prompt_to_file(prompt, f'./prompts/variations_of_default/gameplay_prompt_{i+1}.json')

if __name__ == "__main__":
    main(10)  # Generate 10 new gameplay prompts