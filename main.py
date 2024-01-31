# Import the required libraries
import os
import telegram
import telegram.ext
from auto1111sdk import StableDiffusionPipeline

# Get the API token from the environment variable
API_TOKEN = os.environ.get("BOT_TOKEN")

# Create an updater and a dispatcher object
updater = telegram.ext.Updater(API_TOKEN)
dispatcher = updater.dispatcher

# Create a stable diffusion pipeline object
# Replace the path with your local safetensors or checkpoint file
pipe = StableDiffusionPipeline("model/safetensors.pth")

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
