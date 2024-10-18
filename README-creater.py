import os

# Define paths to the scripts and image directories
script_folder = "."
image_folder = "plots"

# Get all scripts
scripts = [f for f in os.listdir(script_folder) if f.endswith(".py")]

# Get all images
images = [f for f in os.listdir(image_folder) if f.endswith((".png", ".jpg", ".jpeg", ".gif"))]

# Function to remove file extensions
def strip_extension(filename):
    return os.path.splitext(filename)[0]

# Function to extract the date from the script filename (first six characters)
def get_script_date(script):
    return script[:6]

# Create a dictionary to match images with scripts
image_dict = {strip_extension(img): img for img in images}

# Sort scripts by date (newest to oldest)
scripts.sort(key=get_script_date, reverse=True)

# Open README file in write mode
with open("README.md", "w") as readme:
    # Write the header for the README
    readme.write("# Script and Image Gallery\n\n")
    readme.write("This table shows the scripts (sorted by date) and their corresponding plots:\n\n")

    # Write table header in markdown
    readme.write("| Script | Plot |\n")
    readme.write("|--------|------|\n")

    # Loop through each script
    for script in scripts:
        script_name = strip_extension(script)
        
        # Check if an image exists for this script
        if script_name in image_dict:
            image_file = image_dict[script_name]
            image_path = os.path.join(image_folder, image_file)
            # Write the script name and image in markdown table format
            readme.write(f"| `{script}` | ![{image_file}]({image_path}) |\n")
