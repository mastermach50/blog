import os

# Get list of articles
md_files = os.listdir("./articles/raw")

# Convert articles from markdown to html using pandoc
for file in md_files:
    filename_without_ext = file.replace(".md", "")
    title = filename_without_ext.replace("-", " ").title()


    os.system(f"pandoc -f markdown -t html --columns 100 --template template.article.html ./articles/raw/{file} -o ./articles/{filename_without_ext}.html")

    print(f"Processed {filename_without_ext}")


# Convert index from markdown to html
os.system(f"pandoc -f markdown -t html --columns 100 --template template.index.html ./index.md -o ./index.html")
print("Processed Index")