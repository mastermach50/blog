import os

def variable_replacement(file):
    with open(file, "r") as f:
        contents = f.read()
    
    with open(file, "w") as f:
        contents = contents.replace("{{{filename_without_ext}}}", filename_without_ext)
        f.write(contents)


# Get list of articles
md_files = os.listdir("./articles/raw")

# Convert articles from markdown to html using pandoc
for file in md_files:
    filename_without_ext = file.replace(".md", "")
    os.system(f"pandoc -f markdown -t html --columns 120 --template template.article.html ./articles/raw/{file} -o ./articles/{filename_without_ext}.html")
    variable_replacement(f"./articles/{filename_without_ext}.html")
    print(f"Processed {filename_without_ext}")

# Convert index from markdown to html
os.system(f"pandoc -f markdown -t html --columns 120 --template template.index.html ./index.md -o ./index.html")

print("Processed Index")