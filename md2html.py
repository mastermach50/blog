import os

# Get list of articles
md_files = os.listdir("./articles/raw")

# Convert articles from markdown to html using pandoc
for file in md_files:
    filename_without_ext = file.replace(".md", "")
    title = filename_without_ext.replace("-", " ").title()


    os.system(f"pandoc -f markdown -t html --standalone --template template.html ./articles/raw/{file} -o ./articles/{filename_without_ext}.html")

    print(f"Processed {filename_without_ext}")