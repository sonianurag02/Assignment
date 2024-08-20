import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Upload training data
def upload_data(file_path):
    with open(file_path, 'r') as file:
        response = openai.File.create(
            file=file,
            purpose='fine-tune'
        )
    return response['id']

# Create fine-tuning job
def create_fine_tune(file_id):
    response = openai.FineTune.create(
        training_file=file_id,
        model='davinci',  # You can choose a different base model if needed
        n_epochs=4
    )
    return response['id']

# Monitor fine-tuning job
def monitor_fine_tune(fine_tune_id):
    response = openai.FineTune.retrieve(id=fine_tune_id)
    return response

# Use fine-tuned model
def get_response(prompt):
    response = openai.Completion.create(
        model='YOUR_FINE_TUNED_MODEL_ID',  # Replace with your fine-tuned model ID
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

if __name__ == '__main__':
    # Upload your data
    file_id = upload_data('training_data.jsonl')
    print(f"Uploaded file ID: {file_id}")

    # Create a fine-tuning job
    fine_tune_id = create_fine_tune(file_id)
    print(f"Fine-tuning job ID: {fine_tune_id}")

    # Monitor fine-tuning job
    status = monitor_fine_tune(fine_tune_id)
    print(f"Fine-tuning job status: {status['status']}")
