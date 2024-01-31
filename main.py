# Import the required libraries
import os
import telegram
import telegram.ext
from auto1111sdk import StableDiffusionPipeline

# Import the argparse library
import argparse

# Create an argument parser object
parser = argparse.ArgumentParser()

# Add the arguments that you want to accept
parser.add_argument("--use-cpu", default="all", help="Use CPU instead of GPU")
parser.add_argument("--precision", default="full", help="Use full precision instead of half precision")
parser.add_argument("--no-half", action="store_true", help="Disable half precision")
parser.add_argument("--skip-torch-cuda-test", action="store_true", help="Skip the torch CUDA test")

# Parse the arguments from the command line
args = parser.parse_args()

# Access the arguments in your script
print(args.use_cpu)
print(args.precision)
print(args.no_half)
print(args.skip_torch_cuda_test)

# Get the API token from the environment variable
API_TOKEN = os.environ.get("6733249388:AAGQRAkMM_PhVqG-7yGMaf0bm4M7-jbMzzo")

# Create an updater and a dispatcher object
updater = telegram.ext.Updater(API_TOKEN)
dispatcher = updater.dispatcher

# Create a stable diffusion pipeline object
# Replace the path with the URL of your model file on Hugging Face
pipe = StableDiffusionPipeline("https://huggingface.co/avidintroverttt122/mori-files/resolve/main/divineelegancemix_V9.safetensors")

# Define a function to handle the /start command
def start(update, context):
    # Send a welcome message
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I am a bot that can generate images from text using stable diffusion. Type /generate followed by a text prompt to see what I can do."
    )

# Define a function to handle the /generate command
def generate(update, context):
    # Get the text prompt from the user input
    prompt = " ".join(context.args)

    # Check if the prompt is empty
    if not prompt:
        # Send an error message
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please provide a text prompt after the /generate command."
        )
        return

    # Send a message indicating that the image generation is in progress
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Generating an image for: " + prompt
    )

    # Generate an image using the stable diffusion pipeline
    # You can adjust the height, width, and steps parameters as needed
    output = pipe.generate_txt2img(prompt=prompt, height=512, width=512, steps=10)

    # Save the image as a png file
    output[0].save("image.png")

    # Send the image to the user
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("image.png", "rb")
    )

    # Optionally, you can also send a gif of the image generation process
    # Uncomment the following lines to do so
    # output[0].save(
    #     "image.gif",
    #     save_all=True,
    #     append_images=output[1:],
    #     duration=100,
    #     loop=0
    # )
    # context.bot.send_animation(
    #     chat_id=update.effective_chat.id,
    #     animation=open("image.gif", "rb")
    # )

# Register the functions as handlers for the corresponding commands
dispatcher.add_handler(telegram.ext.CommandHandler("start", start))
dispatcher.add_handler(telegram.ext.CommandHandler("generate", generate))

# Start the bot
updater.start_polling()
