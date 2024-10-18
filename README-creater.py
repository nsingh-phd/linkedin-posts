import os

image_folder = "plots"

# Open the README file in write mode
with open("README.md", "w") as readme:
    # Write the header for the README
    readme.write("# Image Gallery\n\n")
    readme.write("This repository contains the following images:\n\n")

    # Loop through each file in the image folder
    for filename in os.listdir(image_folder):
        # Check if the file is an image (extensions can vary)
        if filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
            # Write the markdown to display the image
            image_path = os.path.join(image_folder, filename)
            readme.write(f"![{filename}]({image_path})\n\n")
